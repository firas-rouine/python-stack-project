from flask_app import app,IMAGES_PATH
from flask import  render_template,request, redirect, session,flash,jsonify
from flask_app.models.institution_model import Institution
from flask_app.models.address_model import Address
from flask_app.models.user import User
from flask_app.models.images_model import Image
from flask_app.models.favory_model import Favory
from flask_app.models.review import Review
from flask_app.models.comment import Comment
from flask_app.models.diploma_models import Diploma
import os,re
import urllib.request
from werkzeug.utils import secure_filename
UPLOAD_FOLDER='flask_app/static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS




# ? ========== Add Institution PAGE ==========

# ? ========== Add Institution PAGE ==========

@app.route("/add_institution")
def show_form():
    user=User.get_by_id({'id':session['user_id']})
    # print('😍😍😍',user.image,'😍😍❤')
    instituion=Institution.get_by_id_creator({'id':session['user_id']})
    return render_template('institution.html',user=user,institution=instituion)

#  ========== create institution --- ACTION

@app.route("/creators/institution", methods=["POST","GET"])
def create():
    if not Institution.validate(request.form):
        if not Address.validate(request.form):
            return redirect("/add_institution")
        return redirect("/add_institution")
    
    
    data = {
        **request.form,
        "creator_id" : session['user_id']
    }
    # Save the institution in DB
    institution_id = Institution.create(data)
    data["institution_id"] = institution_id
    Address.create(data)
    
   


    # ? *************************save the new diploma program*****************************
    count=1
    
    data['diploma']=''
    data['program_tittle']=''
    data['description']=''
    
    while ('diploma'+str(count)) in request.form: 
        data={
            "institution_id":institution_id,
            'diploma':request.form['diploma'+str(count)],
            'program_tittle':request.form['program_tittle'+str(count)],
            'description':request.form['description'+str(count)]
        } 
        # if not Diploma.validate(data):
        #     return redirect("/add_institution")
        
        dip=Diploma.create(data)
        count+=1
    # ? **************************************************************************************

   
    # ! *************add images**************
    
    files = request.files.getlist('files[]')   
   
    for file in files:
        print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",len(files))
        if len(files)==1:
            
            data['name_image']='user-circle-light.png'
            
            Image.create(data)
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data['name_image']=filename
            session['image']=IMAGES_PATH+filename
            
            Image.create(data)
            
    flash('files succesfully uploaded')
    return redirect('/add_institution')
    # ! *************************************
    

# ? ========== Edit Institution =================
@app.route('/edit/<int:institution_id>')
def edit_institution(institution_id):
    if 'user_id' not in session:
        return redirect('/')
    institution= Institution.get_by_id_institution({'id': institution_id})
    images=Image.get_by_id({'id': institution_id})
    adresses=Address.get_by_id({'id': institution_id})
    diplomas=Diploma.get_by_id({'id': institution_id})
    user=User.get_by_id({'id':session['user_id']})
    session['institution_id']= institution
    return render_template('edit_institution.html',institution=institution,adresses=adresses,diplomas=diplomas,images=images,user=user)
    

@app.route('/institution/edit', methods=['post'])
def edit():
    inst_data= {
        **request.form,
        'id': session['institution_id']
    }
    Institution.update(inst_data)
    if not Institution.validate(request.form):
        return redirect('/edit/<int:institution_id>_')
    return redirect('/profile')

@app.route('/delete/<int:image_id>')
def delete_image(image_id):
    Image.delete_img_inst({'id':image_id})
    







# ? ========== show Institution ==========

@app.route("/show_institution/<int:id>")
def show_inst(id):
    data = {
        'id' :id,
        'user_id' :session['user_id'] 
    }
    institution = Institution.get_by_id(data)
    data['institution_id'] = institution.id
    session['institution_id']=institution.id
    fav =  Favory.check_favory(data)
    user_review = Review.check_review(data)
    comments = Comment.get_all_comments(data)
    reviews = Review.get_by_id(data)
    global_rate = Review.total_rate(reviews)
    images = Image.get_images_institution(data)
    diplomas = Diploma.get_institution_diplomas(data)
    address = Address.get_address_by_inst_id(data)
    return render_template("show_institution.html",institution=institution, fav=fav,user_review=user_review, comments=comments, global_rate=global_rate,images=images,diplomas=diplomas,address=address)


# =================== add new review =====================
@app.route("/add_reviews/<int:id>", methods=["post"])
def reviews(id):
    data = {
        'institution_id': id,
        'user_id' :session['user_id'],
        'rate' : int(request.form['rate'])
    }
    Review.create(data)
    return redirect(f"/show_institution/{id}")


# =================== add new favory =====================
@app.route("/add_favory/<int:id>")
def add_favory(id):
    data = {
        'user_id' :session['user_id'],
        'institution_id' : id,
    }
    Favory.create(data)
    return redirect(f"/show_institution/{id}")


# =================== add new comment =====================
@app.route("/add_comment/<int:id>", methods=["post"])
def add_comment(id):
    data = {
        **request.form,
        'user_id' : session['user_id'],
        'id' : session['user_id'],
        'institution_id' : id,
    }
    print('/////////////////////////////////////////////')
    Comment.create(data)
    user=User.get_by_id(data)
    # Create a response dictionary
    response = {'full_name': user.first_name +" "+ user.last_name, 'comment': request.form['comment']}
    # Return a JSON response
    return jsonify(response)


