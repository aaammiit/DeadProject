from django.shortcuts import render
from App.models import *
import plotly.graph_objects as go
import plotly.express as px
from django.core.cache import cache
import pandas as pd
from datetime import datetime,timedelta,date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



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
        filtered_df = df[df["KRIMA_type"].isin(["Penalty Notices", "Infringements or Investigations"])]
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

        # Graph: Yearly penalties
        fig = go.Figure(data=[
            go.Scatter(
                x=grouped_yearly_data["Year"],
                y=grouped_yearly_data["KRIMA_imposed_penalty_USD"],
                text=grouped_yearly_data["KRIMA_imposed_penalty_USD"].round(1).astype(str) + "M",
                textposition=text_positions,
                mode="lines+markers+text",
                line=dict(color="rgba(135, 200, 235, 0.8)", width=4),
                marker=dict(size=9, color="green", symbol="circle"),
                textfont=dict(size=11, color="darkgreen", family="Arial"),
            )
        ])
        fig.update_layout(
            title_text="Imposed Monetary Fine (in USD)",
            title_x=0.5,
            xaxis=dict(tickvals=grouped_yearly_data["Year"], showgrid=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=600,
            height=430,
            plot_bgcolor="rgba(0,0,0,0)",
        )

        # Graph: Areas of regulation
        fig1 = go.Figure(data=[
            go.Bar(
                y=top_areas['Krima_Area_of_regulation'],
                x=top_areas['percentage'],
                orientation='h',
                marker=dict(color='rgba(135, 200, 235, 0.8)'),
                text=top_areas['percentage'].astype(str) + '%',
                textposition='outside',
            )
        ])
        fig1.update_layout(
            title="Most Regulated Areas of Regulation",
            width=600,
            height=430,
            margin=dict(r=0),
            yaxis=dict(autorange="reversed", showgrid=False),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
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

    try:
        # Fetch all data from the database
        filedata = krimaCompanyData.objects.all()

        # Filter and process data
        for item in filedata:
            try:
                if (
                    typ == 'Enforcement Actions'
                    and hasattr(item, 'KRIMA_type')
                    and item.KRIMA_type in ['Disciplinary Proceedings','Disciplinary proceedings' ,'Penalty Notices', 'Infringements or Investigations']
                ):
                    enforce_data.append(item)

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
            compnayLen[item.Company_Name] = compnayLen.get(item.Company_Name, 0) + 1
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
    enforceData = ['Disciplinary Proceedings','Disciplinary proceedings' ,'Penalty Notices', 'Infringements or Investigations']
    filetrData = []
    country, regulatory, industry, regulation_set, noticeType, penaltyType, company = (
        set(), set(), set(), set(), set(), set(), set()
    )
    cuntryLen={}
    compnayLen={}
    regLen={}
    try:
        # Fetch all data from the database
        filedata = krimaCompanyData.objects.all()
        

        # Process data
        for item in filedata:
            try:
                # Filter by enforcement data type
                if getattr(item, 'KRIMA_type', '') in enforceData:
                    filetrData.append(item)

                    # Populate sets with unique values
                    if getattr(item, 'rbCountry', ''):
                        country.add(item.rbCountry)
                        

                    if getattr(item, 'Regulatory', ''):
                        regulatory.add(item.Regulatory)
                        
                    if getattr(item, 'Company_Name', ''):
                        company.add(item.Company_Name)
            

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
        
        # Process remaining enforce_data entries
        for item in enforce_data:
            if hasattr(item, 'rbCountry') and item.rbCountry:
                cuntryLen[item.rbCountry] = cuntryLen.get(item.rbCountry, 0) + 1

            if hasattr(item, 'Company_Name') and item.Company_Name:
                compnayLen[item.Company_Name] = compnayLen.get(item.Company_Name, 0) + 1
            
            if hasattr(item, 'Regulatory') and item.Regulatory:
                regLen[item.Regulatory] = regLen.get(item.Regulatory, 0) + 1

        

        # Filter companies with occurrences >= 2
        filtered_compnay = {key: value for key, value in compnayLen.items()}
        

        return filetrData, filtered_compnay, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company, cuntryLen,regLen

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
            if getattr(item, 'Company_Name', '') in selected_company
        ]

    return filtered_data

@login_required
def filterData(request):
    try:
        # Fetch and process data
        filetrData, filtered_compnay, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company, cuntryLen,regLen = fetch_and_process_data()

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
            filtered_data = apply_filters(
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

            return render(request, 'enforceHtml/enforceFilter.html', {
                
                'data': filtered_data,  # Adjust pagination if necessary
                    'lenData':filetrData,
                    'rangeDate': rangeDate,
                    'country': sorted(country),
                'regulatory': sorted(regulatory),
                # 'company': sorted(company),
                'noticeType': sorted(noticeType),
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
    filetrData, filtered_compnay, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company, cuntryLen, regLen = fetch_and_process_data()
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
                'countryName':findcountry
            })

@login_required
def findCompany(request,cmpny):
    findcompnay=cmpny
    filetrData, filtered_compnay, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company, cuntryLen, regLen = fetch_and_process_data()
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
        if i.Company_Name == findcompnay:
            companyData.append(i) 
    companyData = sorted(companyData, key=lambda x: x.Date, reverse=True) 
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
                'countryName':findcompnay
            })


@login_required
def findReg(request,reg):
    findreg=reg
    filetrData, filtered_compnay, rangeDate, country, regulatory, industry, regulation_set, noticeType, penaltyType, company, cuntryLen, regLen = fetch_and_process_data()
    graph_html = cache.get('graph_html')
    graph_html1 = cache.get('graph_html1')
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
    regData = sorted(regData, key=lambda x: x.Date, reverse=True) 
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
                'countryName':findreg
            })
