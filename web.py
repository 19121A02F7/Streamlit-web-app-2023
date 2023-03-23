import streamlit as st
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px
from streamlit_login_auth_ui.widgets import __login__
import os
import streamlit as st

# EDA Pkgs
import pandas as pd

# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import base64
from PIL import Image
from stegano import lsb
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Smart grid data",
                       page_icon=":zap:",
                       layout="wide"
)

__login__obj = __login__(auth_token = "courier_auth_token",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    selected = option_menu(
    menu_title="Main Menu",  # required
    options=["Home","Summary","Projects","Analysis","Security","Contact"],  # required
    icons=["house","vinyl","book","graph-up-arrow","shield-lock","envelope"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
    )


#--------------------------------------------------Home------------------------------------------------#



    if selected == "Home":
        def add_bg_from_local(image_file):
            with open(image_file, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            st.markdown(
            f"""
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Smart Grid</title>
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;600;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
            <section class="header">
            <div class="text-box">
                <h1>Smart Grid Data</h1>
                 <p>A smart grid is a modern electric grid with a two-way flow of electricity and data between power utilities and consumers</p>
                 <a href="https://seleritysas.com/blog/2019/12/09/what-is-smart-grid-big-data-analytics/#:~:text=The%20smart%20grid%20produces%20large,smart%20grid%20big%20data%20analytics." class="hero-btn">Explore</a>
            </div>
            </section>
            </body>
            <style>
            .text-box{{
              width: 100%;
              color: #fff;
              position: absolute;
              top: 10%;
              left: -2%;
              transform: translate (-50%, -50%);
              text-align: center;
             }}
             .text-box h1{{
              font-size:100px;
             }}
             .text-box p{{
              margin: 10px 0px 40px;
              left: 10%;
              font-size: 19px;
             }}
             .hero-btn{{
              display: inline-block;
              text-decoration: none;
              color: #fff;
              border: 8px solid #fff;
              padding: 12px 34px;
              font-size: 18px;
              background: transparent;
              position: relative;
              cursor: pointer;
             }}
             .hero-btn:hover{{
              border: 1px solid #0de95a;
              background: #97f205;
              transition: 1s;
             }}
            .stApp {{
                background-image: linear-gradient(rgba(0,0,0, 0.7),rgba(0,0,0,0.7)),url(data:image/{"png"};base64,{encoded_string.decode()});
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
            )
        add_bg_from_local('pic.png')


#--------------------------------------------Summary----------------------------------------------#
    if selected == "Summary":
        st.title(f"You have selected {selected}")



#-------------------------------------------------- projects------------------------------------------#


    if selected == "Projects":
        st.markdown("##")

        @st.cache_data()
        def get_data_from_csv():
            df = pd.read_csv('Book1.csv')
            #add hour column
            df["hour"]=pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
            return df
        df=get_data_from_csv()

        #------SIDEBAR-------
        st.sidebar.header("Please Filter Here:")
        LCLid=st.sidebar.multiselect(
            "Select the Meter ID:",
            options=df["LCLid"].unique(),
            default=df["LCLid"].unique()
        )

        Date=st.sidebar.multiselect(
            "Select the Date:",
            options=df["Date"].unique(),
            default=df["Date"].unique()
        )

        Time=st.sidebar.multiselect(
            "Select the Time:",
            options=df["Time"].unique(),
            default=df["Time"].unique()
        )

        df_selection=df.query(
            "LCLid==@LCLid & Date==@Date & Time==@Time"
        )


        #------Main page-----
        st.title(":bar_chart: Meter Data Dashboard")
        st.markdown("##")

        #------TOP KPI's
        total_energy=int(df_selection["KWH/hh"].sum())
        average_energy=round(df_selection["KWH/hh"].mean(),2)
        max_energy=round(df_selection["KWH/hh"].max(),2)

        left_column, middle_column, right_column=st.columns(3)
        with left_column:
            st.subheader("Total Energy:")
            st.subheader(f"{total_energy:,} KWH")
        with middle_column:
            st.subheader("Maximun Energy:")
            st.subheader(f"{max_energy:,} KWH")

        with right_column:
            st.subheader("Average Energy:")
            st.subheader(f"{average_energy} KWH")

        st.markdown("---")


        # PIE CHART 1
        df=get_data_from_csv()
        fig_meter_energy=px.pie(
            df, values='KWH/hh', names='LCLid',title='Meter-Energy Data',
        )


        # BAR CHART 2

        energy_by_date=(df_selection.groupby(by=["Date"]).sum()[["KWH/hh"]].sort_values(by="Date")
            )
        fig_date_energy=px.line(
            energy_by_date,
            x=energy_by_date.index,
            y="KWH/hh",
            orientation="h",
            title="<b>Energy by Date</b>",
            color_discrete_sequence=["#734f96"]*len(energy_by_date),
            template="seaborn",
        )


        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_meter_energy, use_container_width=True)
        right_column.plotly_chart(fig_date_energy, use_container_width=True)

        # BAR CHART 3

        energy_by_meterid=(df_selection.groupby(by=["Time"]).sum()[["KWH/hh"]].sort_values(by="Time")
            )
        fig_meter_energy=px.bar(
            energy_by_meterid,
            x=energy_by_meterid.index,
            y="KWH/hh",
            orientation="v",
            title="<b>Energy by Time</b>",
            color_discrete_sequence=["#0083B8"]*len(energy_by_meterid),
            template="seaborn",
        )


        # BAR CHART 4

        energy_by_date=(df_selection.groupby(by=["LCLid"]).sum()[["KWH/hh"]].sort_values(by="LCLid")
            )
        fig_date_energy=px.histogram(
            df, x="LCLid", y="KWH/hh", color='Acorn_grouped', title="<b>Energy for Grouped Categories</b>"
        )


        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_meter_energy, use_container_width=True)
        right_column.plotly_chart(fig_date_energy, use_container_width=True)



        #remove extras

        # hide_st_style="""
        #             <style>
        #             #MainMenu{visibility: hidden;}
        #             footer{visibility: hidden;}
        #             header{visibility: hidden;}
        #             </style>
        #             """
        # st.markdown(hide_st_style, unsafe_allow_html=True)


#--------------------------------------------Analysis----------------------------------------------#
    if selected == "Analysis":
        def main():
         """ Data Analysis """
         st.title("Smart Meter Data Analysis")
         st.subheader("Datasets For ML Explorer")

         #html_temp = """
         #<div style="background-color:none;"><p style="color:skyblue;font-size:50px;padding:10px">Meter Datasets</p></div>
         #"""#
         #st.markdown(html_temp,unsafe_allow_html=True)#

         def file_selector(folder_path='./datasets'):
           filenames = os.listdir(folder_path)
           selected_filename = st.selectbox("Select A file",filenames)
           return os.path.join(folder_path,selected_filename)

         filename = file_selector()
         st.info("You Selected {}".format(filename))

         # Read Data
         df = pd.read_csv(filename)
         # Show Dataset

         if st.checkbox("Show Dataset"):
           number = st.number_input("Number of Rows to View")
           st.dataframe(df.head(number))

         # Show Columns
         if st.button("Column Names"):
           st.write(df.columns)

         # Show Shape
         if st.checkbox("Shape of Dataset"):
           data_dim = st.radio("Show Dimension By ",("Rows","Columns"))
           if data_dim == 'Rows':
             st.text("Number of Rows")
             st.write(df.shape[0])
           elif data_dim == 'Columns':
             st.text("Number of Columns")
             st.write(df.shape[1])
           else:
             st.write(df.shape)

         # Select Columns
         if st.checkbox("Select Columns To Show"):
           all_columns = df.columns.tolist()
           selected_columns = st.multiselect("Select",all_columns)
           new_df = df[selected_columns]
           st.dataframe(new_df)

         # Show Values
         if st.button("Value Counts"):
           st.text("Value Counts By Target/Class")
           st.write(df.iloc[:,-1].value_counts())


         # Show Datatypes
         if st.button("Data Types"):
           st.write(df.dtypes)



         # Show Summary
         if st.checkbox("Summary"):
           st.write(df.describe().T)

         ## Plot and Visualization

         st.subheader("Data Visualization")
         # Correlation
         # Seaborn Plot
         if st.checkbox("Correlation Plot[Seaborn]"):
           st.write(sns.heatmap(df.corr(),annot=True))
           st.pyplot()


         # Pie Chart
         if st.checkbox("Pie Plot"):
           all_columns_names = df.columns.tolist()
           if st.button("Generate Pie Plot"):
             st.success("Generating A Pie Plot")
             st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
             st.pyplot()

         # Count Plot
         if st.checkbox("Plot of Value Counts"):
           st.text("Value Counts By Target")
           all_columns_names = df.columns.tolist()
           primary_col = st.selectbox("Primary Columm to GroupBy",all_columns_names)
           selected_columns_names = st.multiselect("Select Columns",all_columns_names)
           if st.button("Plot"):
             st.text("Generate Plot")
             if selected_columns_names:
               vc_plot = df.groupby(primary_col)[selected_columns_names].count()
             else:
               vc_plot = df.iloc[:,-1].value_counts()
             st.write(vc_plot.plot(kind="bar"))
             st.pyplot()


         # Customizable Plot

         st.subheader("Customizable Plot")
         all_columns_names = df.columns.tolist()
         type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box","kde"])
         selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)

         if st.button("Generate Plot"):
           st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

           # Plot By Streamlit
           if type_of_plot == 'area':
             cust_data = df[selected_columns_names]
             st.area_chart(cust_data)

           elif type_of_plot == 'bar':
             cust_data = df[selected_columns_names]
             st.bar_chart(cust_data)

           elif type_of_plot == 'line':
             cust_data = df[selected_columns_names]
             st.line_chart(cust_data)

           # Custom Plot
           elif type_of_plot:
             cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
             st.write(cust_plot)
             st.pyplot()

         if st.button("Thanks"):
           st.balloons()

         st.sidebar.header("About App")
         st.sidebar.info("A Simple EDA App for Exploring Common ML Dataset")

         st.sidebar.header("Get Datasets")
         st.sidebar.markdown("[Common ML Dataset Repo]("")")

         st.sidebar.header("About")
         st.sidebar.info("Jesus Saves@JCharisTech")
         st.sidebar.text("Built with Streamlit")
         st.sidebar.text("Maintained by Jesse JCharis")


        if __name__ == '__main__':
         main()




#--------------------------------------------Security----------------------------------------------#

    if selected == "Security":

        # Upload file function
        def upload_file():
            file = st.file_uploader("Upload file", type=["csv", "txt", "docx", "pdf", "jpg", "jpeg", "png"])
            if file:
                file_contents = file.read()
                return file, file_contents
            else:
                return None, None

        # Main Streamlit app
        def main():
            # Set up Streamlit app
            st.title("Steganography for Secure File Transfer")
            # Upload file
            file, file_contents = upload_file()
            if file:
                # Ask for cover image
                st.write("Choose a cover image to embed the file into:")
                cover_image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
                if cover_image:
                    # Open the cover image
                    cover_image = Image.open(cover_image)
                    # Embed the file into the image
                    embedded_image = encode_file(file_contents, cover_image)
                    # Display the embedded image
                    st.write("Embedded image:")
                    st.image(embedded_image)
                    # Ask to retrieve file
                    retrieve = st.checkbox("Retrieve file?")
                    if retrieve:
                        # Decode the file from the embedded image
                        retrieved_file = decode_file(embedded_image)
                        # Save the retrieved file
                        with open(file.name, "wb") as f:
                            f.write(retrieved_file)
                        # Display a download link for the retrieved file
                        st.write("Download the retrieved file:")
                        st.download_button(file.name, retrieved_file)

        # Run the Streamlit app
        if __name__ == "__main__":
            main()

#------------------------------------------------- Comtact -----------------------------------------#

    if selected == "Contact":
        st.markdown("---")
        st.header(":mailbox: Get In Touch With Me!")
        contact_form = """
        <form action="https://formsubmit.co/bigdatasmartgrid@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
        </form>
        """

        st.markdown(contact_form, unsafe_allow_html=True)
        # Use Local CSS File
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


        local_css("style.css")
