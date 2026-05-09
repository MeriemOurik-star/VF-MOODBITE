"""
controllers/dashboard_controller.py — DashboardController
Handles: /dashboard  /dashboard/orders  /dashboard/stats  /dashboard/update-status
         /dashboard/stream  (SSE for live orders)
Matches UML: getCommandes(), getStats()
Matches SD6 + SD7 sequence diagrams
"""

import json
import time
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, jsonify,
    Response, stream_with_context
)

from models.commande import Commande, STATUTS_VALIDES
from services.firebase_service import firebase_service
from config import config

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# ---------------------------------------------------------------------------
# GET /dashboard  — Main restaurant dashboard view
# SD6: onSnapshot() → Nouvelle commande reçue → Affiche dans le dashboard
# ---------------------------------------------------------------------------

@dashboard_bp.route("/")
def dashboard():
    lang    = request.args.get("lang", session.get("lang", config.DEFAULT_LANG))
    orders  = firebase_service.get_orders(limit=50)
    stats   = firebase_service.get_stats()

    return render_template(
        "dashboard.html",
        orders         = orders,
        stats          = stats,
        statuts_valides = STATUTS_VALIDES,
        lang           = lang,
        mood_meta      = config.MOOD_META,
    )


# ---------------------------------------------------------------------------
# GET /dashboard/orders  — JSON list of all recent orders (API)
# SD6: Consulter les commandes → Dashboard
# ---------------------------------------------------------------------------

@dashboard_bp.route("/orders")
def get_orders():
    limit  = int(request.args.get("limit", 50))
    orders = firebase_service.get_orders(limit=limit)
    return jsonify({"ok": True, "orders": orders, "count": len(orders)})


# ---------------------------------------------------------------------------
# GET /dashboard/stats  — Aggregated stats (API)
# SD7: getStats() → données agrégées
# ---------------------------------------------------------------------------

@dashboard_bp.route("/stats")
def get_stats():
    stats = firebase_service.get_stats()
    if not stats:
        lang = session.get("lang", config.DEFAULT_LANG)
        msg  = (
            "No stats available yet 📊"
            if lang == "en" else
            "Aucune statistique disponible pour le moment 📊"
        )
        return jsonify({"ok": False, "message": msg, "stats": {}}), 200

    return jsonify({"ok": True, "stats": stats})


# ---------------------------------------------------------------------------
# POST /dashboard/update-status  — Change order status
# SD6: updateOrder(id, { statut: 'En préparation' }) → Firestore → Confirmation
# ---------------------------------------------------------------------------

@dashboard_bp.route("/update-status", methods=["POST"])
def update_status():
    lang   = session.get("lang", config.DEFAULT_LANG)
    data   = request.get_json(silent=True) or {}
    doc_id = data.get("doc_id", "").strip()
    statut = data.get("statut", "").strip().lower()

    if not doc_id:
        return jsonify({"ok": False, "error": "Missing doc_id"}), 400

    if statut not in STATUTS_VALIDES:
        return jsonify({
            "ok":    False,
            "error": f"Invalid status. Allowed: {STATUTS_VALIDES}"
        }), 400

    try:
        firebase_service.update_order_status(doc_id, statut)
    except Exception as e:
        return jsonify({
            "ok":    False,
            "error": ("Update failed, try again 😬"
                      if lang == "en" else
                      "Mise à jour échouée, réessaie 😬")
        }), 500

    # Also update Realtime DB live mirror
    try:
        firebase_service._rtdb.child("commandes_live").child(
            doc_id.replace("-", "_")
        ).update({"statut": statut})
    except Exception:
        pass   # non-critical

    return jsonify({
        "ok":     True,
        "doc_id": doc_id,
        "statut": statut,
        "message": (
            f"Order updated → {statut} ✅"
            if lang == "en" else
            f"Commande mise à jour → {statut} ✅"
        ),
    })


# ---------------------------------------------------------------------------
# GET /dashboard/stream  — Server-Sent Events for live order push
# SD6: Firebase Realtime DB → SSE → Dashboard browser
# The frontend JS subscribes to this endpoint to receive live updates
# without polling.
# ---------------------------------------------------------------------------

@dashboard_bp.route("/stream")
def stream():
    def event_generator():
        """
        Polls Firestore every 5 s and pushes new/changed orders as SSE.
        In production swap this for a proper async push using firebase
        on_snapshot + a queue, but this works reliably with standard Flask.
        """
        seen_ids = set()

        # Initial snapshot
        orders = firebase_service.get_orders(limit=30)
        for o in orders:
            seen_ids.add(o.get("_id", o.get("numeroCommande", "")))

        yield f"data: {json.dumps({'type': 'connected', 'count': len(orders)})}\n\n"

        while True:
            time.sleep(5)
            try:
                latest = firebase_service.get_orders(limit=30)
                new_orders = []
                for o in latest:
                    oid = o.get("_id", o.get("numeroCommande", ""))
                    if oid not in seen_ids:
                        seen_ids.add(oid)
                        new_orders.append(o)

                if new_orders:
                    payload = json.dumps({
                        "type":   "new_orders",
                        "orders": new_orders,
                        "count":  len(new_orders),
                    })
                    yield f"data: {payload}\n\n"
                else:
                    # Heartbeat to keep connection alive
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"

            except GeneratorExit:
                break
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
                time.sleep(10)

    return Response(
        stream_with_context(event_generator()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control":  "no-cache",
            "X-Accel-Buffering": "no",    # disable nginx buffering
        }
    )


# ---------------------------------------------------------------------------
# GET /dashboard/order/<doc_id>  — Single order detail (API)
# SD6: Consulte le détail de la commande → Affiche N°, nom, humeur, plats…
# ---------------------------------------------------------------------------

@dashboard_bp.route("/order/<doc_id>")
def get_order_detail(doc_id):
    try:
        orders = firebase_service.get_orders(limit=200)
        order  = next((o for o in orders if o.get("_id") == doc_id), None)
        if not order:
            return jsonify({"ok": False, "error": "Order not found"}), 404
        return jsonify({"ok": True, "order": order})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
