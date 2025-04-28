from django.shortcuts import render,redirect
from .models import *
import json
import datetime
import pandas as pd
import plotly.graph_objects as go
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
# Create your views here.

from datetime import datetime
from datetime import datetime
import json
from .models import Database, krimaCompanyData

def parse_date(date_str):
    try:
        if date_str:
            return datetime.fromisoformat(date_str)
        return None
    except (ValueError, TypeError):
        print(f"Invalid date format: {date_str}")
        return None

def process_uploaded_database_files():
    # Fetch all files in the Database model
    database_files = Database.objects.all()

    for db_file in database_files:
        file_path = db_file.dataBaseFile.path
        try:
            # Open and load the JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                records = json.load(f)  # Assuming JSON contains a list of objects
                
                if not isinstance(records, list):
                    print(f"Invalid JSON format in file: {file_path}")
                    continue
                
                # Save records to the krimaCompanyData model
                for record in records:
                    krimaCompanyData.objects.create(
                        Unique_ID=record.get("Unique_ID"),
                        rbID=record.get("rbID"),
                        Unique_REC_ID=record.get("Unique_REC_ID"),
                        rbCountry=record.get("rbCountry"),
                        rbContinent=record.get("rbContinent"),
                        rbState=record.get("rbState"),
                        Regulatory=record.get("Regulatory"),
                        RegFullName=record.get("rbFullname"),
                        Date=parse_date(record.get("Date")),
                        Date1=parse_date(record.get("Date_1")),
                        Title=record.get("Title"),
                        URL=record.get("URL"),
                        Article=record.get("Article"),
                        gpt_type=record.get("gpt_type"),
                        GPT_Description_Automated_0=record.get("GPT_Description_Automated_0"),
                        GPT_Description_Automated_1=record.get("GPT_Description_Automated_1"),
                        Company_Name=record.get("Company_Name"),
                        Parent_Company_Name=record.get("Parent_Company_Name"),
                        Entity_Status=record.get("Entity_Status"),
                        Imposed_Civil_Penalty=record.get("Imposed_Civil_Penalty"),
                        Disgorgement_Restitution_Amount=record.get("Disgorgement_&_Restitution_Amount"),
                        Prejudgement_Interest_Amount=record.get("Prejudgement_Interest_Amount"),
                        Total_Imposed_Penalty=record.get("Total_Imposed_Penalty"),
                        Settled_Value=record.get("Settled_Value"),
                        Currency_Code=record.get("Currency_Code"),
                        Non_Monetary_Penalty=record.get("Non-Monetary_Penalty"),
                        New_Title=record.get("New_Title"),
                        Summary=record.get("Summary"),
                        Area_of_activity_or_service=record.get("Area_of_activity_or_service"),
                        Area_of_regulation=record.get("Area_of_regulation"),
                        Error=record.get("Error"),
                        KRIMA_researcher=record.get("KRIMA_researcher"),
                        KRIMA_status=record.get("KRIMA_status"),
                        KRIMA_true_false=record.get("KRIMA_true_false"),
                        KRIMA_type=record.get("KRIMA_type"),
                        KRIMA_notes=record.get("KRIMA_notes"),
                        KRIMA_edited_gpt_person_or_business=record.get("KRIMA_edited_gpt_person_or_business"),
                        KRIMA_edited_gpt_company_check=record.get("KRIMA_edited_gpt_company_check"),
                        Krima_Segmentation_Researcher=record.get("Krima_Segmentation_Researcher"),
                        Krima_Area_of_activity_or_service=record.get("Krima_Area_of_activity_or_service"),
                        Krima_Area_of_regulation=record.get("Krima_Area_of_regulation"),
                        Krima_Segmentation_Status=record.get("Krima_Segmentation_Status"),
                        KRIMA_Segmentation_notes=record.get("KRIMA_Segmentation_notes"),
                        KRIMA_civil_penalty_validated=record.get("KRIMA_civil_penalty_validated"),
                        KRIMA_civil_penalty_cleansed=record.get("KRIMA_civil_penalty_cleansed"),
                        KRIMA_currency=record.get("KRIMA_currency"),
                        KRIMA_civil_penalty_usd=record.get("KRIMA_civil_penalty_usd"),
                        KRIMA_disgorgement_restitution_local_currency=record.get("KRIMA_disgorgement_restitution_local_currency"),
                        KRIMA_disgorgement_restitution_USD=record.get("KRIMA_disgorgement_restitution_USD"),
                        KRIMA_prejudgement_interest_local_currency=record.get("KRIMA_prejudgement_interest_local_currency"),
                        KRIMA_prejudgement_interest_USD=record.get("KRIMA_prejudgement_interest_USD"),
                        KRIMA_imposed_penalty_local_currency=record.get("KRIMA_imposed_penalty_local_currency"),
                        KRIMA_imposed_penalty_USD=record.get("KRIMA_imposed_penalty_USD"),
                        KRIMA_settled_value=record.get("KRIMA_settled_value"),
                        KRIMA_percentage_discount=record.get("KRIMA_percentage_discount"),
                        KRIMA_non_monetary_penalty=record.get("KRIMA_non_monetary_penalty"),
                        Sanctioned_Entity=record.get("Sanctioned_Entity"),
                        Entity_Classification=record.get("Entity_Classification"),
                        Type_of_RC=record.get("Type_of_RC"),
                        Effective_Date=parse_date(record.get("Effective_Date")),
                        Compliance_Timeline=record.get("Compliance_Timeline"),
                        Status=record.get("Status"),
                        Classification=record.get("Classification"),
                        Comment_Deadline=record.get("Comment_Deadline"),
                        Rule_Regualtion_Act=record.get("Rule_Regualtion_Act"),
                        Regulatory_Authority_or_Speaker=record.get("Regulatory_Authority_or_Speaker"),
                        Designation=record.get("Designation"),
                        Compliance_Challenges_or_Key_Regulatory_Concerns=record.get("Compliance_Challenges_or_Key_Regulatory_Concerns"),
                        Regulatory_Impact_or_Expected_Compliance_Outcome=record.get("Regulatory_Impact_or_Expected_Compliance_Outcome"),
                        Jurisdiction_Body=record.get("Jurisdiction_Body"),
                        Case_Number=record.get("Case_Number"),
                        Total_Debt=record.get("Total_Debt"),
                        Applicant=record.get("Applicant"),
                        Respondent=record.get("Respondent"),
                    )
            print(f'Successfully processed and saved data from: {file_path}')
        
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

        # Delete the processed file
        db_file.delete_file()
        print(f'Deleted file: {file_path}')


        

from django.shortcuts import render
import pandas as pd
import plotly.graph_objects as go
from .models import *  # Import your model

def Home(request):
    # Initialize sets for unique values
    country, regulatory, industry, regulation, noticeType, penaltyType, company = (
        set(), set(), set(), set(), set(), set(), set()
    )

    # Attempt to process uploaded database files
    try:
        process_uploaded_database_files()
    except Exception as e:
        print(f"Error processing uploaded database files: {e}")

    try:
        # Fetch all data from the companyData model
        data = krimaCompanyData.objects.all()
        Frontdata = krimaCompanyData.objects.all().order_by('-Date')[:10]  # Latest 10 entries
        rangedate = data[:12]  # First 12 entries

        # Iterate through all items to populate sets
        for item in data:
            try:
                if hasattr(item, 'rbCountry') and item.rbCountry:
                    country.add(item.rbCountry)

                if hasattr(item, 'Regulatory') and item.Regulatory:
                    regulatory.add(item.Regulatory)

                if hasattr(item, 'Company_Name') and item.Company_Name:
                    company.add(item.Company_Name)

                if hasattr(item, 'KRIMA_type') and item.KRIMA_type:
                    noticeType.add(item.KRIMA_type)

                if hasattr(item, 'KRIMA_non_monetary_penalty') and item.KRIMA_non_monetary_penalty:
                    penaltyType.update(map(str.strip, item.KRIMA_non_monetary_penalty.split(',')))

                if hasattr(item, 'Krima_Area_of_activity_or_service') and item.Krima_Area_of_activity_or_service:
                    industry.update(map(str.strip, item.Krima_Area_of_activity_or_service.split(',')))

                if hasattr(item, 'Krima_Area_of_regulation') and item.Krima_Area_of_regulation:
                    regulation.update(map(str.strip, item.Krima_Area_of_regulation.split(',')))
            except Exception as e:
                print(f"Error processing item: {e}")
                continue

        # Convert data into a Pandas DataFrame
        df = pd.DataFrame(list(data.values()))

        # Filter and clean the data
        filtered_df = df[df["KRIMA_type"].isin(["Penalty Notices", "Infringements or Investigations"])]
        filtered_df["Total_Imposed_Penalty"] = pd.to_numeric(filtered_df["Total_Imposed_Penalty"], errors="coerce")
        filtered_df = filtered_df.dropna(subset=["Total_Imposed_Penalty"])
        filtered_df["Date"] = pd.to_datetime(filtered_df["Date"], errors="coerce")
        filtered_df = filtered_df.dropna(subset=["Date"])
        filtered_df["Year"] = filtered_df["Date"].dt.year.astype(int)

        # Group by year and sum penalties
        grouped_yearly_data = filtered_df.groupby("Year", as_index=False)["Total_Imposed_Penalty"].sum()

        # Format the penalties for display
        def format_human_readable(num):
            if num >= 1_000_000_000:
                return f"{int(num // 1_000_000_000)}B"
            elif num >= 1_000_000:
                return f"{int(num // 1_000_000)}M"
            elif num >= 1_000:
                return f"{int(num // 1_000)}K"
            else:
                return str(int(num))

        grouped_yearly_data["Formatted_Penalty"] = grouped_yearly_data["Total_Imposed_Penalty"].apply(format_human_readable)
        grouped_yearly_data["Year"] = grouped_yearly_data["Year"].astype(str)

        # Create a Plotly graph
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=grouped_yearly_data["Year"],
                y=grouped_yearly_data["Total_Imposed_Penalty"],
                text=grouped_yearly_data["Formatted_Penalty"],
                mode="lines+markers+text",
                line=dict(color="blue", width=2),
                marker=dict(size=30, color="red", symbol="circle"),
                textfont=dict(size=8, color="black"),
                texttemplate="<b>%{text}</b>",
            )
        )
        fig.update_layout(
            title_text="Year-wise Penalty",
            title_x=0.5,
            xaxis=dict(title="Year"),
            yaxis=dict(title="Total Penalty USD (in millions)"),
            width=1000,
            height=430,
            plot_bgcolor="rgba(220,242,240,0.5)",
        )

        # Generate HTML for the chart
        graph_html = fig.to_html(full_html=False)

        # Render the template
        return render(request, 'index.html', {
            'data': Frontdata,
            'lenData': data,
            'rangedate': rangedate,
            'country': sorted(country),
            'regulatory': sorted(regulatory),
            'company': sorted(company),
            'noticeType': sorted(noticeType),
            'industry': sorted(industry),
            'regulation': sorted(regulation),
            'penaltyType': sorted(penaltyType),
            'graph_html': graph_html,  # Pass the graph HTML to the template
        })
    except Exception as e:
        print(f"Error in processing data: {e}")
        return render(request, 'error.html', {"message": "An error occurred while processing data."})


def createAccount(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')  # Corrected the confirmation password field name
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('account')  # Redirect after showing message
        
        if password == cpassword:
            try:
                user = User.objects.create_user(username=username, password=password, email=username)
                webUser.objects.create(user=user)
                messages.success(request, 'Account created successfully!')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                return redirect('createAccount')  # Redirect after showing error
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('createAccount')  # Redirect after showing error
    
    return render(request,'main/sineup.html')


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username or password is empty
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('/')  # Redirect to the login page

        try:
            # Attempt to authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Successful login
                request.session['uid'] = user.id  # Storing user ID in the session
                login(request, user)  # Logging in the user
                return redirect('/')  # Redirect to home page after successful login
            else:
                # Invalid credentials
                messages.error(request, 'Username or password does not match.')
                return redirect('login')  # Redirect back to the login page if authentication fails

        except ValidationError as ve:
            # Catch validation errors (e.g., incorrect user data)
            messages.error(request, f'Error: {str(ve)}')
            return redirect('login')  # Redirect to login page on validation error
        except Exception as e:
            # Catch all other exceptions
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('login')  # Redirect back to the login page in case of any error

    # If it's a GET request or after handling POST request
    return render(request,'main/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def pricingPage(request):
    return render(request,'pricing.html')

def Payment(request):
    return render(request,'pricing.html')

def Contact(request):
    return render(request,'contact.html')
