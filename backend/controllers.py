from flask import Flask, render_template,jsonify,session
from flask import current_app as app
from .models import *
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import or_, and_
from datetime import datetime


def get_info(user_id):


    user = User.query.get(user_id)
    return user


@app.route('/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        existing_user = User.query.filter_by(username=username, password=password).first()

        if existing_user:
            if existing_user.flag == True:
                return "You have been marked flagged. Kindly contact the admin."
            session.clear()
            session['user_id'] = existing_user.id
            if existing_user.type == 'influencer':
                return redirect(url_for('idashboard'))
            elif existing_user.type == 'sponsor':
                return redirect(url_for('sdashboard'))
            elif existing_user.type == 'admin':
                return redirect(url_for('adashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')



@app.route('/iregister',methods=['GET','POST'])
def iregister():
    session.clear()
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        reach = request.form['reach']
        category = request.form['category']
        facebook_id = request.form['facebook_id']
        instagram_id = request.form['instagram_id']
        twitter_id = request.form['twitter_id']
        linkedin_id = request.form['linkedin_id']
        youtube_id = request.form['youtube_id']
        tiktok_id = request.form['tiktok_id']
        pinterest_id = request.form['pinterest_id']
        reddit_id = request.form['reddit_id']



        existing_user = User.query.filter_by(email=email,type='influencer').first()
        if existing_user:
            session['user_id'] = existing_user.id
            return redirect(url_for('idashboard'))
        new_influencer = Influencer(email=email, username=username, password=password, bio=bio,reach=reach,category=category,
                                    facebook_id=facebook_id, instagram_id=instagram_id, twitter_id=twitter_id,
                                    linkedin_id=linkedin_id, youtube_id=youtube_id, tiktok_id=tiktok_id,
                                    pinterest_id=pinterest_id, reddit_id=reddit_id)
        db.session.add(new_influencer)
        db.session.commit()
        session['user_id'] = new_influencer.id
        return redirect(url_for('idashboard'))
    return render_template('influencerreg.html')


@app.route('/idashboard',methods=['GET', 'POST'])
def idashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        u=get_info(session['user_id'])
        return render_template('idashboard.html',id=u.id,username=u.username,bio=u.bio,reach=u.reach,category=u.category,facebook_id=u.facebook_id, instagram_id=u.instagram_id,twitter_id=u.twitter_id,linkedin_id=u.linkedin_id,youtube_id=u.youtube_id,tiktok_id=u.tiktok_id,pinterest_id=u.pinterest_id,reddit_id=u.reddit_id)
    else:
        return redirect(url_for('login'))




@app.route('/sregister',methods=['GET','POST'])
def sregister():
    session.clear()
    if request.method == 'POST':
        email = request.form['email']
        username=request.form['username']
        password = request.form['password']
        industry = request.form['industry']
        bio = request.form['bio']


        existing_user = User.query.filter_by(email=email,type='sponsor').first()
        if existing_user:
            return redirect(url_for('login'))
        new_sponsor = Sponsor(email=email, username=username, password=password, industry=industry, bio=bio)
        db.session.add(new_sponsor)
        db.session.commit()
        session['user_id'] = new_sponsor.id
        return redirect(url_for('sdashboard'))
    return render_template('sponsorreg.html')






@app.route('/sdashboard',methods=['GET','POST'])
def sdashboard():
    u=get_info(session['user_id'])
    if request.method=='POST':
        campaign_name=request.form['campaign-name']
        campaign_description=request.form['campaign-description']
        campaign_budget=int(request.form['campaign-budget'])
        campaign_start_date=datetime.strptime(request.form['start-date'], '%Y-%m-%d')
        campaign_end_date=datetime.strptime(request.form['start-date'], '%Y-%m-%d')
        campaign_visibility=request.form['visibility']
        sponsor_id=u.id

        new_campaign = Campaign(name=campaign_name, description=campaign_description, budget=campaign_budget, start_date=campaign_start_date, end_date=campaign_end_date, visibility=campaign_visibility,sponsor_id=sponsor_id)
        db.session.add(new_campaign)
        db.session.commit()
        return render_template('sdashboard.html',id=u.id,username=u.username,bio=u.bio,industry=u.industry)
    return render_template('sdashboard.html',id=u.id,username=u.username,bio=u.bio,industry=u.industry)


@app.route('/iupdate',methods=['GET', 'POST'])
def iupdate():
    u = get_info(session['user_id'])
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        reach = request.form['reach']
        category = request.form['category']
        facebook_id = request.form['facebook_id']
        instagram_id = request.form['instagram_id']
        twitter_id = request.form['twitter_id']
        linkedin_id = request.form['linkedin_id']
        youtube_id = request.form['youtube_id']
        tiktok_id = request.form['tiktok_id']
        pinterest_id = request.form['pinterest_id']
        reddit_id = request.form['reddit_id']


        user=User.query.filter(User.id==u.id).first()
        if username:
            user.username=username
        if password:
            user.password=password
        if bio:
            user.bio=bio
        if reach:
            user.reach=reach
        if category:
            user.category=category
        if facebook_id:
            user.facebook_id=facebook_id
        if instagram_id:
            user.instagram_id=instagram_id
        if twitter_id:
            user.twitter_id=twitter_id
        if linkedin_id:
            user.linkedin_id=linkedin_id
        if youtube_id:
            user.youtube_id=youtube_id
        if tiktok_id:
            user.tiktok_id=tiktok_id
        if pinterest_id:
            user.pinterest_id=pinterest_id
        if reddit_id:
            user.reddit_id=reddit_id

        db.session.commit()
        return redirect(url_for('idashboard'))
    return render_template('iupdate.html')



@app.route('/supdate',methods=['GET', 'POST'])
def supdate():
    u = get_info(session['user_id'])
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        industry = request.form['industry']


        user=User.query.filter(User.id==u.id).first()
        if username:
            user.username=username
        if password:
            user.password=password
        if bio:
            user.bio=bio
        if industry:
            user.industry=industry

        db.session.commit()
        return redirect(url_for('sdashboard'))
    return render_template('supdate.html')


@app.route('/active_campaigns', methods=['GET'])
def get_active_campaigns():
    active_campaigns = Campaign.query.filter(Campaign.end_date >= datetime.now(), Campaign.sponsor_id==session['user_id']).all()
    campaigns_data = []
    for campaign in active_campaigns:
        campaigns_data.append({
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'budget': campaign.budget,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'visibility': campaign.visibility
        })
    return jsonify({'active_campaigns': campaigns_data})



@app.route('/campaigns')
def campaigns():
    campaigns_data =Campaign.query.filter(Campaign.end_date >= datetime.now(), Campaign.sponsor_id==session['user_id'] and Campaign.flag==False).all()
    return render_template('campaigns.html',campaigns=campaigns_data)

@app.route('/campaigns/<int:id>')
def view_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    return render_template('view_campaign.html', campaign=campaign)

@app.route('/campaigns/<int:id>/edit', methods=['GET', 'POST'])
def edit_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    if request.method == 'POST':
        campaign.name = request.form['name']
        campaign.description = request.form['description']
        campaign.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        campaign.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        campaign.budget = request.form['budget']
        campaign.visibility = request.form['visibility']
        db.session.commit()
        return redirect(url_for('campaigns'))
    return render_template('edit_campaign.html', campaign=campaign)

@app.route('/campaigns/<int:id>/delete', methods=['POST','DELETE'])
def delete_campaign(id):
    if request.method=='POST':
        campaign = Campaign.query.get_or_404(id)
        db.session.delete(campaign)
        db.session.commit()
        return redirect(url_for('campaigns'))

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':

        search_term = request.form['search_term']
        category = request.form['category']
        filtered_users = Influencer.query.filter(or_(Influencer.category == '', Influencer.category == category),or_(Influencer.username.ilike(f'%{search_term}%'),Influencer.email.ilike(f'%{search_term}%')))
        return render_template('ssearch.html', filtered_users=filtered_users)
    return render_template('ssearch.html')


@app.route('/ad-requests/<int:influencer_id>', methods=['GET', 'POST'])
def create_ad_request(influencer_id):
    if request.method == 'POST':
        campaign_id = request.form['campaign_id']
        message = request.form['message']
        requirements = request.form['requirements']
        payment_amount = request.form['payment_amount']

        ad_request = AdRequest(
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            messages=message,
            requirements=requirements,
            payment_amount=payment_amount,
            status='Pending'
        )
        db.session.add(ad_request)
        db.session.commit()
        return redirect(url_for('sdashboard'))
    return render_template('create_ad.html', influencer_id=influencer_id)




@app.route('/ads',methods=['GET', 'POST'])
def ads():
    ad_requests = AdRequest.query.filter(AdRequest.influencer_id == session['user_id']).all()
    if request.method == 'POST':
        ad_id = request.form['ad_id']
        action = request.form['action']
        if action == 'accept':
            ad = AdRequest.query.get(ad_id)
            ad.status = 'Accepted'
            db.session.commit()
            return redirect(url_for('ads'))
        elif action == 'reject':
            ad = AdRequest.query.get(ad_id)
            ad.status = 'Rejected'
            db.session.commit()
            return redirect(url_for('ads'))
        elif action == 'negotiate':
            ad = AdRequest.query.get(ad_id)
            ad.payment_amount = request.form['negotiated_amount']
            db.session.commit()
            return redirect(url_for('ads'))
    return render_template('ads.html', ad_requests=ad_requests)


@app.route('/search_campaigns',methods=['GET', 'POST'])
def search_campaigns():
    if request.method=='POST':
        search_term = request.form['search_term']
        budget = request.form['budget']
        campaigns = Campaign.query.filter(or_(Campaign.name.ilike(f'%{search_term}%'), and_(Campaign.budget >= budget, Campaign.visibility == 'public',Campaign.flag == False))).all()

        return render_template('search_campaigns.html', campaigns=campaigns)
    return render_template('search_campaigns.html')


@app.route('/create_ad_request_infl/<int:sponsor_id>',methods=['GET','POST'])
def create_ad_request_infl(sponsor_id):
    if request.method == 'POST':

        campaign_id = request.form['campaign_id']
        message = request.form['message']
        requirements = request.form['requirements']
        payment_amount = request.form['payment_amount']

        ad_request = AdRequest(
            campaign_id=campaign_id,
            sponsor_id=sponsor_id,
            influencer_id= session['user_id'],
            messages=message,
            requirements=requirements,
            payment_amount=payment_amount,
            status='Pending'
        )
        db.session.add(ad_request)
        db.session.commit()
        return redirect(url_for('idashboard'))
    return render_template('create_ad_infl.html', sponsor_id=sponsor_id)


@app.route('/ads_details',methods=['GET', 'POST'])
def ads_details():
    all_ads = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == session['user_id']).all()
    accepted_ads=AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == session['user_id'],AdRequest.status=='Accepted').all()
    rejected_ads=AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == session['user_id'],AdRequest.status=='Rejected').all()
    pending_ads=AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == session['user_id'],AdRequest.status=='Pending').all()
    return render_template('ads_details.html', all_ads=all_ads, accepted_ads=accepted_ads, rejected_ads=rejected_ads, pending_ads=pending_ads)

@app.route('/delete_ad/<int:id>', methods=['POST'])
def delete_ad(ad_id):
    ad=AdRequest.query.get(ad_id)
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('ads_details'))

@app.route('/adashboard',methods=['GET','POST'])
def adashboard():

    users=User.query.all()
    campaigns=Campaign.query.all()
    if request.method == 'POST':
        campaign_id= request.form.get('campaign_id')
        user_id= request.form.get('user_id')
        action= request.form.get('action')
        action_user=request.form.get('action_user')
        if action=='view':
            campaign = Campaign.query.get(campaign_id)
            return render_template('view_campaign_admin.html', campaign=campaign)
        elif action=='flag':
            campaign = Campaign.query.get(campaign_id)
            campaign.flag = True
            db.session.commit()
            return redirect(url_for('adashboard'))
        elif action=='unflag':
            campaign = Campaign.query.get(campaign_id)
            campaign.flag = False
            db.session.commit()
            return redirect(url_for('adashboard'))


        if action_user=='view':
            user = User.query.get(user_id)
            return render_template('view_user_admin.html', user=user)
        elif action_user=='flag':
            user = User.query.get(user_id)
            user.flag = True
            db.session.commit()
            return redirect(url_for('adashboard'))
        elif action_user=='unflag':
            user = User.query.get(user_id)
            user.flag = False
            db.session.commit()
            return redirect(url_for('adashboard'))


    return render_template('adashboard.html',users=users,campaigns=campaigns)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
