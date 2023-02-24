import streamlit as st
from PIL import Image
import pandas as pd
import base64
import uuid
from PIL import Image
import os
import matplotlib.pyplot as plt
import time 
from sklearn.metrics import silhouette_score
from sklearn import metrics 
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import davies_bouldin_score


def set_style():
    st.markdown(
        f"""
        <style>
            .reportview-container {{
                background: #333333;
                color: #FFFFFF;
            }}
            a {{
                color: #FFA500;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_style()

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    if png_file is None:
        return
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Define the background image for the homepage
homepage_bg = './home_page_logo1.jpg'

# Set the background image for the homepage
set_background(homepage_bg)



# Define the black background for subcategory pages
black_bg = Image.new('RGB', (1, 1), color='black')
black_bg_path = f'{uuid.uuid4()}.png'
black_bg.save(black_bg_path)

pink_bg = Image.new('RGB', (1, 1), color='pink')
pink_bg_path = f'{uuid.uuid4()}.png'
pink_bg.save(pink_bg_path)

logo = Image.open("./logo-removebg-preview.png")

logo_resized = logo.resize((250, 200))

# Load the dataframe
df_sorted = pd.read_csv("./df_sorted.csv")
df_X = pd.read_csv("./X.csv")

df_truelabel = pd.read_csv("./true_label.csv")

df_labels = pd.read_csv("./labels.csv")
df_kmeans = pd.read_csv("./kmeans_labels.csv")

# Define the categories and subcategories
categories = ['Home', 'Topwear', 'Bottom wear', 'Shoes', 'Accessories', 'Customer Reviews', 'About', 'Contact', 'Newsletter', 'Evaluation metrics']
subcategories = {
    'Topwear': ['Shirts', 'Jackets','Dresses'],
    'Bottom wear': ['Trousers'],
    'Shoes': ['Sneakers', 'Ankle boots', 'Heels', 'Sandals'],
    'Accessories': ['Mini bags', 'Large bags']
}

subcategory = None

# Create the sidebar menu
category = st.sidebar.selectbox('Select a category', categories)

# Display the homepage
if category == 'Home':
    set_background(homepage_bg)
elif category == 'Contact':
    set_background(black_bg_path)
    st.write('## Contact Us')
    name = st.text_input("Full Name")
    st.write(name)
    email = st.text_input("Email")
    st.write(email)
    message = st.text_area("Message")
    st.write(message)
    if st.button('Contact Us'):
        st.write('Thank you for contacting us! We read every message and typically respond within 48 hours if a reply is required.')     
elif category == 'Newsletter':
    set_background(black_bg_path)
    st.write('## Subscribe to our Newsletter')
    st.write('Sign up to receive email updates on new product announcements, gift ideas, special promotions, sales and more. ')
    name = st.text_input("Full Name")
    st.write(name)
    email = st.text_input("Email")
    st.write(email)
    if st.button('SIGN UP'):
        st.write('Thank you for signing up to our newsletter. You now have exclusive access to the latest product launches at SuitsMe and have access to special promotions in the future!')
elif category == 'About':
    set_background(black_bg_path)
    st.write('# About Us')
    st.write('## Our Company')
    st.write("""
    SuitsMe is a global fashion company that is dedicated to providing high-quality and stylish clothing for men and women. Our company prides itself on our commitment to our customers and our unique business model, which includes design, production, distribution, and sales.
    """)
    st.write("## Our Team")
    
    # Set the path to the directory containing the photos
    photos_dir = './my_photos'
    
    # Define a dictionary that maps photo filenames to names and positions
    names = {
        'aradhya_rathi_face.jpeg': 'Aradhya Rathi - CEO',
        'solene_dh_face.jpeg': 'Solene Dhanani - CTO',
        'radi_face.jpeg': 'Radi - CFO',
        'zelong_face.jpeg': 'Zelong Qin - Wellbeing Officer',
        'lat_face.jpeg': 'Laeticia El Khoury - Marketing Director',
        'owen_chen_face.jpeg': 'Owen Chen - Head of Outreach',
        'nadine_face.jpeg': 'Nadine - HR Head'
    }
    
    # Get a list of all the files in the directory
    files = os.listdir(photos_dir)
    
    # Filter the list to include only JPEG files
    files = [f for f in files if f.endswith('.jpeg')]
    
    # Sort the list of files so that the specified photos are on top
    specified_files = ['aradhya_rathi_face.jpeg', 'solene_dh_face.jpeg', 'radi_face.jpeg']
    files.sort(key=lambda f: specified_files.index(f) if f in specified_files else len(specified_files))
    
    # Display the photos and names in a grid layout with 3 photos per row
    col1, col2, col3 = st.columns(3)
    for i, file in enumerate(files):
        if i % 3 == 0:
            col = col1
        elif i % 3 == 1:
            col = col2
        else:
            col = col3
        
        # Open the photo file using PIL and display it
        with open(os.path.join(photos_dir, file), 'rb') as f:
            img = Image.open(f)
            col.image(img, use_column_width=True)
            
        # Display the name and position of the person below the photo
        name = names.get(file, '')
        col.write(name)
elif category == 'Customer Reviews':
    set_background(pink_bg_path)
    st.write('# Customer Reviews')
    st.write('## Add your customer review below')
    message = st.text_area("Message")
    st.write(message)
    if st.button('Add'):
        st.write('Thank you for the review. We will upload it soon.')
    # Define a list of dictionaries, where each dictionary represents a review
    reviews = [
        {
            'text': "I recently had an amazing shopping experience with SuitsMe, a fashion clothing company that offers a wide selection of trendy and stylish clothes. From the moment I landed on their website, I was impressed by how easy it was to find exactly what I was looking for.",
            'author': 'Jessica',
            'position': 'Fashion Blogger'
        },
        {
            'text': "The website was well-organized and user-friendly, making it simple for me to navigate and locate my desired products. I appreciated that they had clothing sizes clearly marked, and the customer reviews helped me choose the right size and style for me.",
            'author': 'Maggie',
            'position': 'Online Shopper'
        },
        {
            'text': "When my order arrived, I was delighted with the quality of the clothing. The fabrics were soft and comfortable, and the clothes fit me perfectly. I received many compliments on my outfit, and I felt stylish and confident.",
            'author': 'Anna',
            'position': 'Fashion Enthusiast'
        },
        {
            'text': "Furthermore, the customer service I received from SuitsMe was exceptional. They were quick to respond to my inquiries, and their support team was friendly and professional. They resolved my concerns with ease and made my shopping experience truly seamless.",
            'author': 'Rachel',
            'position': 'Customer Support'
        },
        {
            'text': "Overall, I highly recommend SuitsMe to anyone who is looking for quality, stylish clothing and excellent customer service. They have exceeded my expectations, and I will definitely be a repeat customer in the future.",
            'author': 'Julie',
            'position': 'Loyal Customer'
        }
    ]
    
    # Display the reviews in pink boxes with italicized text
    col1, col2 = st.columns(2)
    for i, review in enumerate(reviews):
        if i % 2 == 0:
            col = col1
        else:
            col = col2
        
        with col:
            st.markdown(f'<div style="background-color: pink; color: black; font-weight: bold; padding: 20px; margin-bottom: 20px;"><em>{review["text"]}</em></div>', unsafe_allow_html=True)
            st.write(f'{review["author"]}, {review["position"]}')

elif category == 'Evaluation metrics':
    
    set_background(black_bg_path)
    
    st.write('# Cluster Quality Metrics')
    
    st.write('## Silhouette Score')
    if st.button('Calculate Silhouette score'):
        with st.spinner('Calculating silhouette score...'):
            start_time = time.time()
            silhouette_avg = silhouette_score(df_X, df_labels)
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
        st.write(f"The silhouette score is: {silhouette_avg:.3f}")
        st.write(f"Time taken: {time_taken:.2f} seconds")
        
    st.write('## Rand Index Score')
    if st.button('Calculate Rand index score'):
        with st.spinner('Calculating rand index score...'):
            start_time = time.time()
            rand_index = metrics.rand_score(df_truelabel.values.ravel(), df_labels.values.ravel())
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
        st.write(f"The Rand index score is: {rand_index:.3f}")
        st.write(f"Time taken: {time_taken:.2f} seconds")

    st.write('## Calinski-Harabasz Score')
    if st.button('Calculate Calinski-Harabasz score'):
        with st.spinner('Calculating Calinski-Harabasz score...'):
            start_time = time.time()
            score = calinski_harabasz_score(df_X, df_kmeans)
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
        st.write(f"The Calinski-Harabasz score is: {score:.3f}")
        st.write(f"Time taken: {time_taken:.2f} seconds")

    st.write('## Davies-Bouldin Index')
    if st.button('Calculate Davies-Bouldin Index'):
        with st.spinner('Calculating Davies-Bouldin Index...'):
            start_time = time.time()
            dbi = davies_bouldin_score(df_X, df_kmeans)
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
        st.write(f"The Davies-Bouldin Index is: {dbi:.3f}")
        st.write(f"Time taken: {time_taken:.2f} seconds")


else:
    set_background(black_bg_path)
    subcategory = st.sidebar.selectbox('Select a sub-category', subcategories[category])


# Handle the subcategory selections and display the images

if subcategory == 'Shirts':
    st.image(logo_resized)
    st.write('## Shirts')
    cluster_num = 9
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    

    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

elif subcategory == 'Sandals':
    st.image(logo_resized)
    st.write('## Sandals')
    cluster_num = 7
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    
    
    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

elif subcategory == 'Jackets':
    st.image(logo_resized)
    st.write('## Jackets')
    cluster_num = 2
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    

    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

elif subcategory == 'Dresses':
    st.image(logo_resized)
    st.write('## Dresses')
    cluster_num = 3
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    
    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

elif subcategory == 'Large bags':
    st.image(logo_resized)
    st.write('## Large bags')
    cluster_num = 4
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    
    
    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

elif subcategory == 'Trousers':
    st.image(logo_resized)
    st.write('## Trousers')
    cluster_num = 6
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    
    
    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

elif subcategory == 'Sneakers':
    st.image(logo_resized)
    st.write('## Sneakers')
    cluster_num = 0
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    
    
    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

elif subcategory == 'Ankle boots':
    st.image(logo_resized)
    st.write('## Ankle boots')
    cluster_num = 8
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    
    
    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number


elif subcategory == 'Heels':
    st.image(logo_resized)
    st.write('## Heels')
    cluster_num = 5
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")
    
    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

elif subcategory == 'Mini bags':
    st.image(logo_resized)
    st.write('## Mini bags')
    cluster_num = 1
    group = df_sorted[df_sorted["cluster"] == cluster_num]
    page_number = st.session_state.get('page_number', 1)
    num_cols = 1
    items_per_page = 100
    start_index = (page_number - 1) * items_per_page
    end_index = page_number * items_per_page
    group = group.iloc[start_index:end_index]
    num_rows = (len(group) - 1) // num_cols + 1
    st.write(f"Page {page_number}")
    st.write(f"Showing {start_index+1} to {end_index} of {len(df_sorted[df_sorted['cluster'] == cluster_num])} products")
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            i = row * num_cols + col
            if i < len(group):
                pixels = group.iloc[i, 2:-1].values.astype('int')
                image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                button_key = f"view_similar_{i}"
                if cols[col].button(label="View 5 Similar products for below", key=button_key):
                    similar_group = df_sorted[df_sorted["cluster"] == cluster_num]
                    similar_group = similar_group.sample(n=5)
                    similar_cols = st.columns(len(similar_group))
                    for j in range(len(similar_group)):
                        pixels = similar_group.iloc[j, 2:-1].values.astype('int')
                        similar_image = Image.fromarray(pixels.reshape((28, 28)).astype('uint8'), mode='L')
                        similar_cols[j].image(similar_image, caption=f"Cluster {cluster_num} - Similar Product {j+1}")
                cols[col].image(image, caption=f"Cluster {cluster_num} - Product Image {start_index + i + 1}")




        
    # Show "Previous Page" button if not on the first page
    if start_index > 0:
        if st.button('Previous Page'):
            page_number -= 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number
    
    # Show "Next Page" button if there are more items to show
    if end_index < len(df_sorted[df_sorted["cluster"] == cluster_num]):
        if st.button('Next Page'):
            page_number += 1
            st.experimental_set_query_params(page=page_number)
            st.session_state['page_number'] = page_number

