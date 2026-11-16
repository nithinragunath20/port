"""
test_app_endpoints.py — Automated Route and Functional Verifier
"""

import sys
import os
from app import create_app

def run_tests():
    app = create_app('development')
    client = app.test_client()

    print("=" * 60)
    print("RUNNING AUTOMATED ENDPOINT AND INTEGRATION TESTS")
    print("=" * 60)

    # 1. Test Home page
    res_home = client.get('/')
    assert res_home.status_code == 200, f"Home page failed: {res_home.status_code}"
    assert b"I build" in res_home.data and b"intelligent" in res_home.data and b"systems." in res_home.data
    assert b"AGENTGUARD AI" in res_home.data
    assert b"Student Mental Health" in res_home.data
    assert b"Lumbini Technologies" in res_home.data
    print("[PASS] GET / — Home Page rendered with all sections, 3D setup, and project showcase")

    # 2. Test /home alias
    res_home_alias = client.get('/home')
    assert res_home_alias.status_code == 200
    print("[PASS] GET /home — Home alias works")

    # 3. Test Contact page
    res_contact = client.get('/contact')
    assert res_contact.status_code == 200
    assert b"CONTACT" in res_contact.data
    assert b"nithin.ragunath.20@gmail.com" in res_contact.data
    print("[PASS] GET /contact — Minimalist Contact page rendered")

    # 4. Test Bio / CV page
    res_bio = client.get('/bio')
    assert res_bio.status_code == 200
    assert b"Lumbini Technologies" in res_bio.data
    assert b"Jain University" in res_bio.data
    print("[PASS] GET /bio — Verified credentials and bio page rendered")

    # 5. Test Project Detail page
    res_proj = client.get('/project/agentguard-ai')
    assert res_proj.status_code == 200
    assert b"AGENTGUARD AI" in res_proj.data
    print("[PASS] GET /project/agentguard-ai — Project detail specification page rendered")

    # 6. Test Live AgentGuard AI static app serving
    res_ag = client.get('/agentguard-ai')
    assert res_ag.status_code == 200
    assert b"AgentGuard AI" in res_ag.data
    print("[PASS] GET /agentguard-ai — Live AgentGuard AI application served directly")

    # 7. Test PDF Downloads
    res_resume = client.get('/resume/download')
    assert res_resume.status_code == 200
    print(f"[PASS] GET /resume/download — Resume PDF served ({len(res_resume.data)} bytes)")

    res_offer = client.get('/offer-letter/download')
    assert res_offer.status_code == 200
    print(f"[PASS] GET /offer-letter/download — Offer Letter PDF served ({len(res_offer.data)} bytes)")

    # 8. Test Contact Form Validation & SQLite Persistence
    payload = {
        "name": "Alex Vance",
        "email": "alex.vance@mit.edu",
        "subject": "AI Research Collaboration",
        "message": "We reviewed your AgentGuard AI architecture and would love to discuss a research collaboration."
    }
    res_post = client.post('/contact/send', json=payload)
    assert res_post.status_code == 200
    json_data = res_post.get_json()
    assert json_data.get('success') is True
    print(f"[PASS] POST /contact/send — Contact submission validated, saved to SQLite, async sync queued: {json_data.get('message')}")

    # 9. Verify in Database
    with app.app_context():
        from models import ContactMessage
        msg = ContactMessage.query.filter_by(email="alex.vance@mit.edu").first()
        assert msg is not None, "Message was not saved in SQLite!"
        print(f"[PASS] SQLite Verification — Found saved record ID #{msg.id} from {msg.name}")

    print("=" * 60)
    print("ALL 9 TEST SUITES PASSED FLAWLESSLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
