from django.shortcuts import render,redirect
from App.models import *
import plotly.graph_objects as go
import plotly.express as px
from django.core.cache import cache
import pandas as pd
from datetime import datetime,timedelta,date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.templatetags.static import static
import json



import pandas as pd
import plotly.graph_objects as go

def generate_graphs(filedata):
    try:
        # Convert filedata to DataFrame
        if isinstance(filedata, list):
            df = pd.DataFrame(filedata)
        else:
            df = pd.DataFrame(list(filedata.values()))

        if df.empty:
            print("DataFrame is empty")
            return None, None

        # Ensure required columns exist
        required_columns = ["KRIMA_type", "KRIMA_imposed_penalty_USD", "Date", "Krima_Area_of_regulation"]
        if not all(col in df.columns for col in required_columns):
            print("Missing required columns in data")
            return None, None

        # Filter and clean data
        filtered_df = df[df["KRIMA_type"].isin(["Penalty Orders", "Infringements or Investigations"])]
        filtered_df["KRIMA_imposed_penalty_USD"] = pd.to_numeric(filtered_df["KRIMA_imposed_penalty_USD"], errors="coerce")
        filtered_df.dropna(subset=["KRIMA_imposed_penalty_USD", "Date"], inplace=True)
        filtered_df["Date"] = pd.to_datetime(filtered_df["Date"], errors="coerce")
        filtered_df.dropna(subset=["Date"], inplace=True)
        filtered_df["Year"] = filtered_df["Date"].dt.year.astype(int)

        # Group data by year
        grouped_yearly_data = (filtered_df.groupby("Year", as_index=False)
                               ["KRIMA_imposed_penalty_USD"].sum().head(5))
        grouped_yearly_data["KRIMA_imposed_penalty_USD"] /= 1_000_000
        grouped_yearly_data["Year"] = grouped_yearly_data["Year"].astype(str)

        # Analyze areas of regulation
        all_areas = filtered_df['Krima_Area_of_regulation'].dropna().str.split(', ').explode()
        area_counts = all_areas.value_counts().reset_index()
        area_counts.columns = ['Krima_Area_of_regulation', 'count']
        total_count = area_counts['count'].sum()
        area_counts['percentage'] = (area_counts['count'] / total_count * 100).round(0).astype(int)
        top_areas = area_counts.head(10)

        # Generate the dynamic text positions
        def calculate_text_position(y_values):
            positions = []
            for i, y in enumerate(y_values):
                if i == 0:
                    positions.append("top center")
                elif i == len(y_values) - 1:
                    positions.append("top left")
                else:
                    if y > y_values[i - 1] and y > y_values[i + 1]:
                        positions.append("top left")
                    else:
                        positions.append("bottom right")
            return positions

        text_positions = calculate_text_position(grouped_yearly_data["KRIMA_imposed_penalty_USD"])

        fig = go.Figure()

        # Initial trace (starting with first point)
        fig.add_trace(go.Scatter(
            x=[grouped_yearly_data["Year"].iloc[0]],  # Start with the first point
            y=[grouped_yearly_data["KRIMA_imposed_penalty_USD"].iloc[0]],
            text=[grouped_yearly_data["KRIMA_imposed_penalty_USD"].iloc[0].round(1).astype(str) + "M"],
            textposition=[text_positions[0]],
            mode="lines+markers+text",
            line=dict(color="rgba(135, 200, 235, 0.8)", width=4),
            marker=dict(size=9, color="green", symbol="circle"),
            textfont=dict(size=11, color="darkgreen", family="Arial"),
        ))

        # Add animation frames (Fix: Ensure full dataset appears)
        frames1 = []
        num_steps = 5  # Increase for smoother effect
        for step in range(1, num_steps +1 ):
            fraction = step / num_steps  # Gradual reveal
            num_points = int(fraction * len(grouped_yearly_data)+2)  # Number of points to reveal

            frames1.append(go.Frame(
                data=[go.Scatter(
                    x=grouped_yearly_data["Year"][:num_points],
                    y=grouped_yearly_data["KRIMA_imposed_penalty_USD"][:num_points],
                    text=grouped_yearly_data["KRIMA_imposed_penalty_USD"][:num_points].round(0).astype(str) + "M",
                    textposition=text_positions[:num_points],
                    mode="lines+markers+text",
                    line=dict(color="rgba(135, 200, 235, 0.8)", width=4),
                    marker=dict(size=9, color="green", symbol="circle"),
                    textfont=dict(size=11, color="darkgreen", family="Arial"),
                )
                
                ]
            ))

        fig.update(frames=frames1)

        # Layout and animation settings
        fig.update_layout(
            title_text="Imposed Monetary Fine (in USD)",
            title_x=0.5,
            xaxis=dict(tickvals=grouped_yearly_data["Year"], showgrid=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=600,
            height=430,
            plot_bgcolor="rgba(0,0,0,0)",
            updatemenus=[] , # No play button, animation auto-starts
        )
        fig.update_layout(
            sliders=[{
                
                "transition": {"duration": 400},
                "currentvalue": {"prefix": "Year: "},
            }]
        )


        color_stages = [
    'rgba(135, 200, 235, 0.8)',  # Light Blue
    'rgba(135, 200, 235, 0.8)',  # Light Green
    'rgba(135, 200, 235, 0.8)',  # Light Yellow
    'rgba(135, 200, 235, 0.8)'   # Final Blue (Original)
]

# Create figure
        fig1 = go.Figure()

        # Initial empty bar
        fig1.add_trace(go.Bar(
            y=top_areas['Krima_Area_of_regulation'],
            x=[0] * len(top_areas),  # Start from 0
            orientation='h',
            marker=dict(color=color_stages[0]),  # Start with first shade
            text=['0%'] * len(top_areas),
            textposition='outside',
        ))

        # Generate animation frames with color transitions
        frames = []
        num_steps = 1 # Number of animation steps
        for i in range(1, num_steps + 1):
            # Determine the color stage based on progress
            color = color_stages[i * len(color_stages) // (num_steps + 1)]
            
            frames.append(go.Frame(data=[go.Bar(
                y=top_areas['Krima_Area_of_regulation'],
                x=(i / num_steps) * top_areas['percentage'],  # Gradual increase
                text=((i / num_steps) * top_areas['percentage']).round(1).astype(str) + '%',
                marker=dict(color=color)  # Change color during animation
            )]))

        # Final frame: Restore original color
        frames.append(go.Frame(data=[go.Bar(
            y=top_areas['Krima_Area_of_regulation'],
            x=top_areas['percentage'],
            text=top_areas['percentage'].astype(str) + '%',
            marker=dict(color=color_stages[-1])  # Final original color
        )]))

        fig1.update(frames=frames)

        # Layout and animation settings
        fig1.update_layout(
            title="Most Regulated Areas of Regulation",
            width=600,
            height=430,
            margin=dict(r=0),
            yaxis=dict(autorange="reversed", showgrid=False),
            xaxis=dict(showgrid=False, zeroline=False, range=[0, max(top_areas['percentage']) * 1.2]),
            plot_bgcolor='rgba(0,0,0,0)',
            updatemenus=[],  # No visible play button
            sliders=[{
                "transition": {"duration": 100,  # Animation duration in milliseconds
            "easing": "cubic-in-out"  # Use a smooth easing function 
            },
                
            }]
        )
        

        # Return HTML for graphs
        return fig.to_html(full_html=False), fig1.to_html(full_html=False)

    except Exception as e:
        print(f"Error creating visualizations: {e}")
        return None, None



@login_required
def enforceType(request, typ):
    # Initialize variables
    enforce_data = []
    country, regulatory, industry, regulation_set, noticeType, penaltyType, company = (
        set(), set(), set(), set(), set(), set(), set()
    )
    cuntryLen = {}
    compnayLen = {}
    regLen = {}
    rbData={}

    try:
        # Fetch all data from the database
        filedata = krimaCompanyData.objects.all()

        # Filter and process data
        for item in filedata:
            try:
                if (
                    typ == 'Enforcement Actions'
                    and hasattr(item, 'KRIMA_type')
                    and item.KRIMA_type in ['Disciplinary Proceedings','Disciplinary proceedings' ,'Penalty Orders', 'Infringements or Investigations']
                ):
                    enforce_data.append(item)
                    rbData[item.rbID] = item.RegFullName 

                    # Collect unique values for filters
                    if item.rbCountry:
                        country.add(item.rbCountry)
                    if item.Regulatory:
                        regulatory.add(item.Regulatory)
                    if item.Company_Name:
                        company.add(item.Company_Name)
                    if item.KRIMA_type:
                        noticeType.add(item.KRIMA_type)
                    if item.KRIMA_non_monetary_penalty:
                        penaltyType.update(map(str.strip, item.KRIMA_non_monetary_penalty.split(',')))
                    if item.Krima_Area_of_activity_or_service:
                        industry.update(map(str.strip, item.Krima_Area_of_activity_or_service.split(',')))
                    if item.Krima_Area_of_regulation:
                        regulation_set.update(map(str.strip, item.Krima_Area_of_regulation.split(',')))
            except AttributeError as e:
                print(f"Skipping item due to missing attribute: {e}")
                continue

        # Prepare data for the template
        enforce_data = sorted(enforce_data, key=lambda x: x.Date, reverse=True)
        Frontdata = enforce_data[:10]
        rangeDate = enforce_data[11:15]
        # Count occurrences
        for item in enforce_data:
            cuntryLen[item.rbCountry] = cuntryLen.get(item.rbCountry, 0) + 1
            compnayLen[item.KRIMA_edited_gpt_company_check] = compnayLen.get(item.KRIMA_edited_gpt_company_check, 0) + 1
            regLen[item.Regulatory] = regLen.get(item.Regulatory, 0) + 1

        # Cache graphs if not already cached
        graph_html = cache.get('graph_html')
        graph_html1 = cache.get('graph_html1')

        if not graph_html or not graph_html1:
            graph_html, graph_html1 = generate_graphs(filedata)
            cache.set('graph_html', graph_html, timeout=3600)
            cache.set('graph_html1', graph_html1, timeout=3600)

        # Render the response
        return render(
            request,
            'enforceHtml/enforcePage.html',
            {
                'data': Frontdata,
                'rangeData': rangeDate,
                'lenData':enforce_data,
                'rbData':rbData,
                'country': sorted(country),
                'regulatory': sorted(regulatory),
                'company': sorted(company),
                'noticeType': sorted(noticeType),
                'industry': sorted(industry),
                'regulation': sorted(regulation_set),
                'penaltyType': sorted(penaltyType),
                'graph_html': graph_html,
                'graph_html1': graph_html1,
                'cuntryLen': cuntryLen,
                'compnayLen': compnayLen,
                'regLen': regLen,
            },
        )
    except Exception as e:
        print(f"Error in enforceType: {e}")
        return render(request, 'error.html', {"message": "An error occurred while processing data."})




def fetch_and_process_data():
    enforceData = ['Disciplinary Proceedings','Disciplinary proceedings' ,'Penalty Orders', 'Infringements or Investigations']
    filetrData = []
    country, regulatory, industry, regulation_set, noticeType, penaltyType, company = (
        set(), set(), set(), set(), set(), set(), set()
    )
    rbData={}
    
    try:
        # Fetch all data from the database
        filedata = krimaCompanyData.objects.all()
        

        # Process data
        for item in filedata:
            try:
                # Filter by enforcement data type
                if getattr(item, 'KRIMA_type', '') in enforceData:
                    filetrData.append(item)
                    rbData[item.rbID] = item.RegFullName

                    # Populate sets with unique values
                    if getattr(item, 'rbCountry', ''):
                        country.add(item.rbCountry)
                        

                    if getattr(item, 'Regulatory', ''):
                        regulatory.add(item.Regulatory)
                        
                    if getattr(item, 'KRIMA_edited_gpt_company_check', ''):
                        company.add(item.KRIMA_edited_gpt_company_check)
            

                    if getattr(item, 'KRIMA_type', ''):
                        noticeType.add(item.KRIMA_type)

                    if getattr(item, 'KRIMA_non_monetary_penalty', ''):
                        penaltyType.update(map(str.strip, item.KRIMA_non_monetary_penalty.split(',')))

                    if getattr(item, 'Krima_Area_of_activity_or_service', ''):
                        industry.update(map(str.strip, item.Krima_Area_of_activity_or_service.split(',')))

                    if getattr(item, 'Krima_Area_of_regulation', ''):
                        regulation_set.update(map(str.strip, item.Krima_Area_of_regulation.split(',')))

            except Exception as e:
                print(f"Error processing item: {e}")
                continue

        # Sort by Date
        enforce_data = sorted(filetrData, key=lambda x: getattr(x, 'Date', datetime.min), reverse=True)
        Frontdata = enforce_data[:10]  # First 10 entries for the front page
        rangeDate = enforce_data[11:15]  # First 12 entries for the Date range
        
        # Filter companies with occurrences >= 2
        
        

        return filetrData, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company,rbData

    except Exception as e:
        print(f"Error in enforceType: {e}")
        return [], [], []

def filter_by_Date_range(filtered_data, fromMonth, fromYear, toMonth, toYear):
    """Filters data by Date range."""
    if fromMonth and fromYear and toMonth and toYear:
        try:
            # Construct Dates
            from_Date_str = f"{fromYear}-{fromMonth}-01"
            to_Date_str = f"{toYear}-{toMonth}-01"

            # Parse Dates
            from_Date = datetime.strptime(from_Date_str, '%Y-%m-%d')
            to_Date = datetime.strptime(to_Date_str, '%Y-%m-%d')

            # Adjust to_Date to the last day of the selected month
            if to_Date.month == 12:
                to_Date = to_Date.replace(day=31)  # December ends on the 31st
            else:
                to_Date = to_Date.replace(month=to_Date.month + 1, day=1) - timedelta(days=1)

            # Check if from_Date is later than to_Date and swap them if needed
            if from_Date > to_Date:
                from_Date, to_Date = to_Date, from_Date

            # Filter data
            return [
                item for item in filtered_data
                if hasattr(item, 'Date') and item.Date and 
                isinstance(item.Date, (datetime, date)) and  # Ensure Date is a valid Datetime or Date
                from_Date.date() <= item.Date <= to_Date.date()
            ]

        except ValueError:
            raise ValueError("Invalid Date range. Please ensure the inputs are correct.")

    return filtered_data


def apply_filters(filtered_data, selected_country, selected_regulatory, selected_industry, selected_regulation,
                  selected_noticeType, selected_penaltyType, selected_company):
    """Apply additional filters based on the user inputs."""

    # Filter by country
    if selected_country:
        filtered_data = [
            item for item in filtered_data
            if getattr(item, 'rbCountry', '') in selected_country
        ]

    # Filter by regulatory body
    if selected_regulatory:
        filtered_data = [
            item for item in filtered_data
            if getattr(item, 'Regulatory', '') in selected_regulatory
        ]

    # Filter by industry
    if selected_industry:
        filtered_data = [
            item for item in filtered_data
            if any(
                str(industry_word).strip().lower() in (getattr(item, 'Krima_Area_of_activity_or_service', '') or '').lower()
                for industry_word in selected_industry
            )
        ]

    # Filter by regulation
    if selected_regulation:
        filtered_data = [
            item for item in filtered_data
            if any(
                str(regulation_word).strip().lower() in (getattr(item, 'Krima_Area_of_regulation', '') or '').lower()
                for regulation_word in selected_regulation
            )
        ]

    # Filter by notice type
    if selected_noticeType:
        filtered_data = [
            item for item in filtered_data
            if getattr(item, 'KRIMA_type', '') in selected_noticeType
        ]

    # Filter by penalty type
    if selected_penaltyType:
        filtered_data = [
            item for item in filtered_data
            if any(
                str(penalty_word).strip().lower() in (getattr(item, 'KRIMA_non_monetary_penalty', '') or '').lower()
                for penalty_word in selected_penaltyType
            )
        ]

    # Filter by company
    if selected_company:
        filtered_data = [
            item for item in filtered_data
            if getattr(item, 'KRIMA_edited_gpt_company_check', '') in selected_company
        ]

    

    return filtered_data

@login_required
def filterData(request):
    cuntryLen={}
    compnayLen={}
    regLen={}
    try:
        
        # Fetch and process data
        filetrData, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company,rbData = fetch_and_process_data()

        if request.method == 'POST':
            # Extract filter inputs
            fromMonth = request.POST.get('fromMonth')
            fromYear = request.POST.get('fromYear')
            toMonth = request.POST.get('toMonth')
            toYear = request.POST.get('toYear')
            selected_country = request.POST.getlist('country')
            selected_regulatory = request.POST.getlist('regulatory')
            selected_industry = request.POST.getlist('industry')
            selected_regulation = request.POST.getlist('regulation')
            selected_noticeType = request.POST.getlist('noticeType')
            # selected_penaltyType = request.POST.getlist('penaltyType')
            # selected_company = request.POST.getlist('company')

            # Filter by Date range
            try:
                filtered_data = filter_by_Date_range(filetrData, fromMonth, fromYear, toMonth, toYear)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)

            # Apply additional filters
            filtered_data= apply_filters(
                filtered_data, selected_country, selected_regulatory, selected_industry, selected_regulation,
                selected_noticeType, '', ''
            )

            
            
            graph_html = cache.get('graph_html')
            graph_html1 = cache.get('graph_html1')
            if not graph_html or not graph_html1:
                # Cache miss: Generate graphs
                filedata = krimaCompanyData.objects.all()
                graph_html, graph_html1 = generate_graphs(filedata)

                # Cache the generated graphs
                cache.set('graph_html', graph_html, timeout=3600)
                cache.set('graph_html1', graph_html1, timeout=3600)

            filtered_data = sorted(filtered_data, key=lambda x: getattr(x, 'Date', datetime.min),reverse=True)
            for item in filtered_data:
                if hasattr(item, 'rbCountry') and item.rbCountry:
                    cuntryLen[item.rbCountry] = cuntryLen.get(item.rbCountry, 0) + 1

                if hasattr(item, 'KRIMA_edited_gpt_company_check') and item.KRIMA_edited_gpt_company_check:
                    compnayLen[item.KRIMA_edited_gpt_company_check] = compnayLen.get(item.KRIMA_edited_gpt_company_check, 0) + 1
                
                if hasattr(item, 'Regulatory') and item.Regulatory:
                    regLen[item.Regulatory] = regLen.get(item.Regulatory, 0) + 1

            filtered_compnay = {key: value for key, value in compnayLen.items()}

            return render(request, 'enforceHtml/enforceFilter.html', {
                
                'data': filtered_data,  # Adjust pagination if necessary
                    'lenData':filetrData,
                    'rangeDate': rangeDate,
                    'country': sorted(country),
                'regulatory': sorted(regulatory),
                # 'company': sorted(company),
                'noticeType': sorted(noticeType),
                'rbData':rbData,
                'industry': sorted(industry),
                'regulation': sorted(regulation_set),
                # 'penaltyType': sorted(penaltyType),
                    'countryData': selected_country,
                    'regulatoryData': selected_regulatory,
                    'industryData': selected_industry,
                    'regulationData': selected_regulation,
                    'noticeData': selected_noticeType,
                    'graph_html': graph_html,
                'graph_html1': graph_html1,
                'cuntryLen':cuntryLen,
                'compnayLen':filtered_compnay,
                'regLen':regLen,
            })

        # return render(request, 'your_template.html', {"filtered_data": filetrData})

    except Exception as e:
        print(f"Error in filterData: {e}")
        return render(request, 'error.html', {"message": "An error occurred while processing data."})


@login_required
def findCountry(request,cntry):
    findcountry=cntry
    cuntryLen={}
    compnayLen={}
    regLen={}
    filetrData, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company,rbData = fetch_and_process_data()
    graph_html = cache.get('graph_html')
    graph_html1 = cache.get('graph_html1')
    if not graph_html or not graph_html1:
        # Cache miss: Generate graphs
        filedata = krimaCompanyData.objects.all()
        graph_html, graph_html1 = generate_graphs(filedata)

        # Cache the generated graphs
        cache.set('graph_html', graph_html, timeout=3600)
        cache.set('graph_html1', graph_html1, timeout=3600)
    

    contryData=[]
    for i in filetrData:
        if i.rbCountry == findcountry:
            contryData.append(i)

    contryData = sorted(contryData, key=lambda x: x.Date, reverse=True) 
    for item in filetrData:
        if hasattr(item, 'rbCountry') and item.rbCountry:
            cuntryLen[item.rbCountry] = cuntryLen.get(item.rbCountry, 0) + 1

        if hasattr(item, 'KRIMA_edited_gpt_company_check') and item.KRIMA_edited_gpt_company_check:
            compnayLen[item.KRIMA_edited_gpt_company_check] = compnayLen.get(item.KRIMA_edited_gpt_company_check, 0) + 1
                
        if hasattr(item, 'Regulatory') and item.Regulatory:
            regLen[item.Regulatory] = regLen.get(item.Regulatory, 0) + 1

    filtered_compnay = {key: value for key, value in compnayLen.items()}  
    return render(request, 'enforceHtml/enforceCtRg.html', {
                
                'data': contryData,  # Adjust pagination if necessary
                    'lenData':filetrData,
                    'rangeDate': rangeDate,
                    'country': sorted(country),
                'regulatory': sorted(regulatory),
                'company': sorted(company),
                'noticeType': sorted(noticeType),
                'industry': sorted(industry),
                'regulation': sorted(regulation_set),
                'penaltyType': sorted(penaltyType),
                'graph_html': graph_html,
                'graph_html1': graph_html1,
                'cuntryLen':cuntryLen,
                'compnayLen':filtered_compnay,
                'regLen':regLen,
                'countryName':findcountry,
                'rbData':rbData
            })

@login_required
def findCompany(request,cmpny):
    findcompnay=cmpny
    cuntryLen={}
    compnayLen={}
    regLen={}
    filetrData, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company,rbData= fetch_and_process_data()
    graph_html = cache.get('graph_html')
    graph_html1 = cache.get('graph_html1')
    if not graph_html or not graph_html1:
        # Cache miss: Generate graphs
        filedata = companyData.objects.all()
        graph_html, graph_html1 = generate_graphs(filedata)

        # Cache the generated graphs
        cache.set('graph_html', graph_html, timeout=3600)
        cache.set('graph_html1', graph_html1, timeout=3600)

    companyData=[]
    for i in filetrData:
        if i.KRIMA_edited_gpt_company_check == findcompnay:
            companyData.append(i) 
    companyData = sorted(companyData, key=lambda x: x.Date, reverse=True) 
    for item in filetrData:
        if hasattr(item, 'rbCountry') and item.rbCountry:
            cuntryLen[item.rbCountry] = cuntryLen.get(item.rbCountry, 0) + 1

        if hasattr(item, 'KRIMA_edited_gpt_company_check') and item.KRIMA_edited_gpt_company_check:
            compnayLen[item.KRIMA_edited_gpt_company_check] = compnayLen.get(item.KRIMA_edited_gpt_company_check, 0) + 1
                
        if hasattr(item, 'Regulatory') and item.Regulatory:
            regLen[item.Regulatory] = regLen.get(item.Regulatory, 0) + 1

    filtered_compnay = {key: value for key, value in compnayLen.items()}
    return render(request, 'enforceHtml/enforceCtRg.html', {
                
                'data': companyData,  # Adjust pagination if necessary
                    'lenData':filetrData,
                    'rangeDate': rangeDate,
                    'country': sorted(country),
                'regulatory': sorted(regulatory),
                'company': sorted(company),
                'noticeType': sorted(noticeType),
                'industry': sorted(industry),
                'regulation': sorted(regulation_set),
                'penaltyType': sorted(penaltyType),
                'graph_html': graph_html,
                'graph_html1': graph_html1,
                'cuntryLen':cuntryLen,
                'compnayLen':filtered_compnay,
                'regLen':regLen,
                'countryName':findcompnay,
                'rbData':rbData
            })


@login_required
def findReg(request,reg):
    findreg=reg
    cuntryLen={}
    compnayLen={}
    regLen={}
    regName=set()
    filetrData, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company,rbData = fetch_and_process_data()
    graph_html = cache.get('graph_html')
    graph_html1 = cache.get('graph_html1')
    regName=set()
    if not graph_html or not graph_html1:
        # Cache miss: Generate graphs
        filedata = krimaCompanyData.objects.all()
        graph_html, graph_html1 = generate_graphs(filedata)

        # Cache the generated graphs
        cache.set('graph_html', graph_html, timeout=3600)
        cache.set('graph_html1', graph_html1, timeout=3600)

    regData=[]
    for i in filetrData:
        if i.Regulatory == findreg:
            regData.append(i)
            regName.add(i.RegFullName)
        
    regData = sorted(regData, key=lambda x: x.Date, reverse=True)
    for item in filetrData:
        if hasattr(item, 'rbCountry') and item.rbCountry:
            cuntryLen[item.rbCountry] = cuntryLen.get(item.rbCountry, 0) + 1

        if hasattr(item, 'KRIMA_edited_gpt_company_check') and item.KRIMA_edited_gpt_company_check:
            compnayLen[item.KRIMA_edited_gpt_company_check] = compnayLen.get(item.KRIMA_edited_gpt_company_check, 0) + 1
                
        if hasattr(item, 'Regulatory') and item.Regulatory:
            regLen[item.Regulatory] = regLen.get(item.Regulatory, 0) + 1

    filtered_compnay = {key: value for key, value in compnayLen.items()}  
    return render(request, 'enforceHtml/enforceCtRg.html', {
                
                'data': regData,  # Adjust pagination if necessary
                    'lenData':filetrData,
                    'rangeDate': rangeDate,
                    'country': sorted(country),
                'regulatory': sorted(regulatory),
                'company': sorted(company),
                'noticeType': sorted(noticeType),
                'industry': sorted(industry),
                'regulation': sorted(regulation_set),
                'penaltyType': sorted(penaltyType),
                'graph_html': graph_html,
                'graph_html1': graph_html1,
                'cuntryLen':cuntryLen,
                'compnayLen':filtered_compnay,
                'regLen':regLen,
                'regName':regName,
                'rbData':rbData
            })



def normalize(name):
    return name.lower().replace(" ", "_").replace("-", "_")

def get_flag_path(country_name):
    if not country_name:
        return ''
    
    flag_dir = os.path.join(settings.BASE_DIR, 'App', 'static', 'images', 'Flags')

    try:
        for file_name in os.listdir(flag_dir):
            name, ext = os.path.splitext(file_name)
            if name.lower() == country_name.lower() and ext.lower() in ['.png', '.jpg', '.jpeg', '.svg', '.webp']:
                relative_path = os.path.join('images', 'Flags', file_name)
                return static(relative_path)
    except FileNotFoundError:
        return ''

    return ''

def get_logo_path(rbid):
    for ext in ['png', 'jpg', 'jpeg', 'svg', 'webp']:
        relative_path = f"images/RB_Logos/{rbid}.{ext}"
        absolute_path = os.path.join(settings.BASE_DIR, 'App', 'static', relative_path)
        if os.path.exists(absolute_path):
            return static(relative_path)
    return ''

@login_required
def enforceRb(request, id):
    rbid = str(id)
    data = []
    AGrowth = None
    cGpd = None
    gdp_data = []
    country_name = None

    # Load profile data
    profile_path = os.path.join(settings.BASE_DIR, 'App', 'RbData', '196_RB_Profiles.json')
    with open(profile_path, 'r') as file:
        fileData = json.load(file)

    # Check if rbid exists in fileData
    for i in fileData:
        if i['rbID'] == rbid:
            data.append(i)
            country_name = i.get('rbCountry')
            break

    # Redirect if rbid not found
    if not data:
        return redirect(request.META.get('HTTP_REFERER', '/typeNews/Enforcement%20Actions'))
 # Redirect back or to home

    # Get logo path
    logo_path = get_logo_path(rbid)

    # Get flag path
    flag_path = get_flag_path(country_name) if country_name else ''

    if country_name:
        norm_name = normalize(country_name)

        # Load GDP-related data
        with open(os.path.join(settings.BASE_DIR, 'App', 'RbData', 'growth.json'), 'r') as f:
            growth_json = json.load(f)

        with open(os.path.join(settings.BASE_DIR, 'App', 'RbData', 'annualGrowth.json'), 'r') as f:
            annual_json = json.load(f)

        with open(os.path.join(settings.BASE_DIR, 'App', 'RbData', 'CountryGDP.json'), 'r') as f:
            country_gdp_json = json.load(f)

        # Extract gdp_data
        for entry in growth_json:
            if normalize(entry.get("Country_Name")) == norm_name:
                expected_years = ['2019', '2020', '2021', '2022', '2023']
                gdp_data = [entry.get(year) for year in expected_years]
                break

        # Extract AGrowth
        for entry in annual_json:
            if normalize(entry.get("Country_Name")) == norm_name:
                AGrowth = entry.get('2023')
                break

        # Extract cGpd
        for entry in country_gdp_json:
            if normalize(entry.get("Country_Name")) == norm_name:
                cGpd = entry.get('2023_USD')
                break

    # Attach GDP & growth to profile data
    data[0]['GDP_2023_USD'] = cGpd
    data[0]['Annual_Growth_2023'] = AGrowth

    return render(request, 'enforceHtml/enforceRb.html', {
        'data': data,
        'logo': logo_path,
        'flag': flag_path,
        'gdp_data': gdp_data,
        'country_name': country_name,
    })