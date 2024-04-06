import streamlit as st
import nltk
import spacy
spacy.load('en_core_web_sm')
nltk.download('stopwords')
import base64, random
import time, datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io, random
from streamlit_tags import st_tags
from PIL import Image
from links import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import pafy


st.set_page_config(
    page_icon= "📄",
    page_title="Resume Score Analyzer",
)

def youtubeLinks(link):
    video = pafy.new(link)
    return video.title

def download_link(dataframe , file , text):
    file_csv = dataframe.to_csv(index = False)
    b64 = base64.b64encode(file_csv.encode()).decode()
    link = f'<a href = "data:file/csv;base64,{b64}" download = "{file}">{text}<a>'
    return link

def pdf(file):
    rm = PDFResourceManager()
    fake_file = io.StringIO()
    convert = TextConverter(rm , fake_file , laparams = LAParams())
    page_in = PDFPageInterpreter(rm , convert)

    with open(file , 'rb') as f:
        for pages in PDFPage.get_pages(f,
                                       caching=True,
                                       check_extractable=True):
            page_in.process_page(pages)
            print(pages)
        text = fake_file.getvalue()

    convert.close()
    fake_file.close()
    return text

def showPDF(filePath):
    with open (filePath , "rb") as file:
        pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def courseRecommend(courseList):
    st.subheader("**Courses & Certificates 📖 to Boost your Resume & Skills**")
    c = 0
    rec_course = []
    reco = st.slider('Choose Number of Course Recommendation:', 1, 10, 4)
    random.shuffle(courseList)
    for c_name , c_link in courseList:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == reco:
            break
    return rec_course

def run():
    st.title("Resume Score Analyzer")
    img = Image.open('logo.jpg')
    img = img.resize((250, 250))
    st.image(img)

    pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
    if pdf_file is not None:
        # with st.spinner('Uploading your Resume....'):
        #     time.sleep(4)
        save_image_path = './' + pdf_file.name
        with open(save_image_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        showPDF(save_image_path)
        resume_data = ResumeParser(save_image_path).get_extracted_data()
        if resume_data:
            ## Get the whole resume data
            resume_text = pdf(save_image_path)

            st.header("**Resume Analysis**")
            st.success("Hello " + resume_data['name'])
            st.subheader("**Your Basic info**")
            try:
                st.text('Name: ' + resume_data['name'])
                st.text('Email: ' + resume_data['email'])
                st.text('Contact: ' + resume_data['mobile_number'])
                st.text('Resume pages: ' + str(resume_data['no_of_pages']))
            except:
                pass
            cand_level = ''
            if resume_data['no_of_pages'] == 1:
                cand_level = "Fresher"
                st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                            unsafe_allow_html=True)
            elif resume_data['no_of_pages'] == 2:
                cand_level = "Intermediate"
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                            unsafe_allow_html=True)
            elif resume_data['no_of_pages'] >= 3:
                cand_level = "Experienced"
                st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                            unsafe_allow_html=True)

            st.subheader("**Skills Recommendation💡**")
            ## Skill shows
            keywords = st_tags(label='### Skills that you have',
                                text='See our skills recommendation',
                                value=resume_data['skills'], key='1')

            ##  recommendation
            ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                            'streamlit']
            web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                            'javascript', 'angular js', 'c#', 'flask']
            android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
            ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
            uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                            'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                            'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                            'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                            'user research', 'user experience']

            recommended_skills = []
            reco_field = ''
            rec_course = ''
            ## Courses recommendation
            for i in resume_data['skills']:
                ## Data science recommendation
                if i.lower() in ds_keyword:
                    print(i.lower())
                    reco_field = 'Data Science'
                    st.success("** Our analysis says you are looking for Data Science Jobs.**")
                    recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                            'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                            'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                            'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                            'Streamlit']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills, key='2')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    rec_course = courseRecommend(ds_course)
                    break

                ## Web development recommendation
                elif i.lower() in web_keyword:
                    print(i.lower())
                    reco_field = 'Web Development'
                    st.success("** Our analysis says you are looking for Web Development Jobs **")
                    recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                            'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills, key='3')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    rec_course = courseRecommend(web_course)
                    break

                ## Android App Development
                elif i.lower() in android_keyword:
                    print(i.lower())
                    reco_field = 'Android Development'
                    st.success("** Our analysis says you are looking for Android App Development Jobs **")
                    recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                            'Kivy', 'GIT', 'SDK', 'SQLite']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills, key='4')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    rec_course = courseRecommend(android_course)
                    break
                    

                ## IOS App Development
                elif i.lower() in ios_keyword:
                    print(i.lower())
                    reco_field = 'IOS Development'
                    st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                    recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                            'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                                            'Auto-Layout']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills, key='5')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    rec_course = courseRecommend(ios_course)
                    break

                ## Ui-UX Recommendation
                elif i.lower() in uiux_keyword:
                    print(i.lower())
                    reco_field = 'UI-UX Development'
                    st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                    recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                            'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                            'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                                            'Solid', 'Grasp', 'User Research']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills, key='6')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)
                    rec_course = courseRecommend(uiux_course)
                    break

            #
            ## Insert into table
            ts = time.time()
            cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            timestamp = str(cur_date + '_' + cur_time)

            ### Resume writing recommendation
            st.subheader("**Resume Tips & Ideas💡**")
            resume_score = 0
            if 'Objective' in resume_text:
                resume_score = resume_score + 20
                st.markdown(
                    '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',
                    unsafe_allow_html=True)

            if 'Declaration' in resume_text:
                resume_score = resume_score + 20
                st.markdown(
                    '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration✍/h4>''',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',
                    unsafe_allow_html=True)

            if 'Hobbies' or 'Interests' in resume_text:
                resume_score = resume_score + 20
                st.markdown(
                    '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies⚽</h4>''',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',
                    unsafe_allow_html=True)

            if 'Achievements' in resume_text:
                resume_score = resume_score + 20
                st.markdown(
                    '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements🏅 </h4>''',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',
                    unsafe_allow_html=True)

            if 'Projects' in resume_text:
                resume_score = resume_score + 20
                st.markdown(
                    '''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects👨‍💻 </h4>''',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h4>''',
                    unsafe_allow_html=True)

            st.subheader("**Resume Score📝**")
            st.markdown(
                """
                <style>
                    .stProgress > div > div > div > div {
                        background-color: #d73b5c;
                    }
                </style>""",
                unsafe_allow_html=True,
            )
            my_bar = st.progress(0)
            score = 0
            for percent_complete in range(resume_score):
                score += 1
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1)
            st.success('** Your Resume Writing Score: ' + str(score) + '**')
            st.warning(
                "** Note: This score is calculated based on the content that you have added in your Resume. **")
            st.balloons()

        
            
        else:
            st.error('Something went wrong..')

run()
