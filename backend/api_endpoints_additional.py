"""
Additional API endpoints for VocalGuard advanced features
"""

# Add these routes to app.py after the existing endpoints

@app.route('/api/report', methods=['POST'])
def report_scam():
    """
    FEATURE 15: Community scam reporting
    
    Report a scam call to the community database
    """
    try:
        data = request.json
        phone_number = data.get('phone_number')
        description = data.get('description', 'Scam call reported')
        risk_score = data.get('risk_score', 75)
        scam_category = data.get('scam_category', 'General Scam')
        
        if not phone_number:
            return jsonify({'error': 'Phone number is required'}), 400
        
        report_id = caller_intelligence.report_scam(
            phone_number, description, risk_score, scam_category
        )
        
        return jsonify({
            'success': True,
            'report_id': report_id,
            'message': 'Scam reported successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/block', methods=['POST'])
def block_number():
    """
    FEATURE 15: Block a phone number
    """
    try:
        data = request.json
        phone_number = data.get('phone_number')
        reason = data.get('reason', 'User blocked')
        
        if not phone_number:
            return jsonify({'error': 'Phone number is required'}), 400
        
        success = caller_intelligence.block_number(phone_number, reason)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Number {phone_number} blocked successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Number already blocked'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/blocklist', methods=['GET'])
def get_blocklist():
    """Get list of blocked numbers"""
    try:
        limit = request.args.get('limit', 100, type=int)
        blocked_numbers = caller_intelligence.get_blocklist(limit)
        
        return jsonify({
            'success': True,
            'blocked_numbers': blocked_numbers,
            'total': len(blocked_numbers)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reputation/<phone_number>', methods=['GET'])
def check_reputation(phone_number):
    """Check caller reputation"""
    try:
        reputation = caller_intelligence.check_number_reputation(phone_number)
        
        return jsonify({
            'success': True,
            'reputation': reputation
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/threats/summary', methods=['GET'])
def get_threat_summary():
    """Get current threat intelligence summary"""
    try:
        summary = threat_intelligence.get_threat_summary()
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

