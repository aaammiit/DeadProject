from django.shortcuts import render
from App.models import *
import pandas as pd
from datetime import datetime,timedelta,date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def fetch_and_process_data():
    speechData = ['Insolvency']
    filetrData = []
    country, regulatory ,Case_Number,Jurisdiction_Body = (
        set(), set(), set(), set()
    )
    cuntryLen={}
    regLen={}
    try:
        # Fetch all data from the database
        filedata = krimaCompanyData.objects.all()
        # Process data
        for item in filedata:
            try:
                # Filter by enforcement data type
                 if getattr(item, 'KRIMA_type', '') in speechData:
                    filetrData.append(item)

                    # Populate sets with unique values
                    if getattr(item, 'rbCountry', ''):
                        country.add(item.rbCountry)
                        
                    if getattr(item, 'Regulatory', ''):
                        regulatory.add(item.Regulatory)
                    
                    if getattr(item, 'Case_Number', ''):
                        Case_Number.add(item.Case_Number)
                        
                    if getattr(item, 'Jurisdiction_Body', ''):
                        Jurisdiction_Body.add(item.Jurisdiction_Body)
                    

            except Exception as e:
                print(f"Error processing item: {e}")
                continue

        # Sort by date
        enforce_data = sorted(filetrData, key=lambda x: getattr(x, 'Date', datetime.min), reverse=True)
        Frontdata = enforce_data[:10]  # First 10 entries for the front page
        rangedate = enforce_data[11:15]  # First 12 entries for the date range
        
        # Process remaining enforce_data entries
        for item in enforce_data:
            if hasattr(item, 'rbCountry') and item.rbCountry:
                cuntryLen[item.rbCountry] = cuntryLen.get(item.rbCountry, 0) + 1
            
            if hasattr(item, 'Regulatory') and item.Regulatory:
                regLen[item.Regulatory] = regLen.get(item.Regulatory, 0) + 1

        return filetrData, rangedate, country, regulatory,cuntryLen,regLen,Jurisdiction_Body, Case_Number

    except Exception as e:
        print(f"Error in enforceType: {e}")
        return [], [], []

@login_required
def insolvencyType(request,typ):
    santion_data = []
    country, regulatory, Jurisdiction_Body , Case_Number= (
        set(), set(), set() ,set()
    )
    cuntryLen = {}
    regLen = {}
    
    try:
        # Fetch all data from the database
        filedata = krimaCompanyData.objects.all()
    

        # Filter and process data
        for item in filedata:
            try:
                if (
                    typ == 'Insolvency'
                    and hasattr(item, 'KRIMA_type')
                    and item.KRIMA_type in ['Insolvency']
                ):
                    santion_data.append(item)

                    # Populate sets with unique values
                    if hasattr(item, 'rbCountry') and item.rbCountry:
                        country.add(item.rbCountry)

                    if hasattr(item, 'Regulatory') and item.Regulatory:
                        regulatory.add(item.Regulatory)
                    
                    if hasattr(item, 'Jurisdiction_Body') and item.Jurisdiction_Body:
                        Jurisdiction_Body.add(item.Jurisdiction_Body)

                    
                    if hasattr(item, 'Case_Number') and item.Case_Number:
                        Case_Number.add(item.Case_Number)

                    
            except Exception as e:
                print(f"Error processing item: {e}")
                continue
        
        # Sort and slice enforce_data by date
        santion_data = sorted(santion_data, key=lambda x: x.Date, reverse=True)
        Frontdata = santion_data[:10]  # First 10 entries for the front page
        rangedate = santion_data[11:15]  # First 12 entries for the date range
        for item in santion_data:
            if hasattr(item, 'rbCountry') and item.rbCountry:
                cuntryLen[item.rbCountry] = cuntryLen.get(item.rbCountry, 0) + 1
            
            if hasattr(item, 'Regulatory') and item.Regulatory:
                regLen[item.Regulatory] = regLen.get(item.Regulatory, 0) + 1

        return render(
            request,
            'insolvency/insolvencyPage.html',
            {
                'data': Frontdata,
                'rangedate': rangedate,
                'lenData': santion_data,
                'country': sorted(country),
                'regulatory': sorted(regulatory),
                'Jurisdiction_Body': sorted(Jurisdiction_Body),
                'Case_Number': sorted(Case_Number),
                'cuntryLen': cuntryLen,
                'regLen':regLen
                
            },
        )
    except Exception as e:
        print(f"Error in enforceType: {e}")
        return render(request, 'error.html', {"message": "An error occurred while processing data."})
    

def filter_by_date_range(filtered_data, fromMonth, fromYear, toMonth, toYear):
    """Filters data by date range."""
    if fromMonth and fromYear and toMonth and toYear:
        try:
            # Construct dates
            from_date_str = f"{fromYear}-{fromMonth}-01"
            to_date_str = f"{toYear}-{toMonth}-01"

            # Parse dates
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d')

            # Adjust to_date to the last day of the selected month
            if to_date.month == 12:
                to_date = to_date.replace(day=31)  # December ends on the 31st
            else:
                to_date = to_date.replace(month=to_date.month + 1, day=1) - timedelta(days=1)

            # Check if from_date is later than to_date and swap them if needed
            if from_date > to_date:
                from_date, to_date = to_date, from_date

            # Filter data
            return [
                item for item in filtered_data
                if hasattr(item, 'Date') and item.Date and 
                isinstance(item.Date, (datetime, date)) and  # Ensure Date is a valid Datetime or Date
                from_date.date() <= item.Date <= to_date.date()
            ]

        except ValueError:
            raise ValueError("Invalid date range. Please ensure the inputs are correct.")

    return filtered_data

def apply_filters(filtered_data, selected_country, selected_regulatory,selected_case_number ,selected_jurisdiction_body):
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

    if selected_case_number:
        filtered_data = [
            item for item in filtered_data
            if getattr(item, 'Case_Number', '') in selected_case_number
        ]

    # Filter by regulatory body
    if selected_jurisdiction_body:
        filtered_data = [
            item for item in filtered_data
            if getattr(item, 'Jurisdiction_Body', '') in selected_jurisdiction_body
        ]

    

    return filtered_data


@login_required
def insolvencyfilterData(request):
    try:
        # Fetch and process data
        filetrData, rangedate, country, regulatory, cuntryLen, regLen , Jurisdiction_Body, Case_Number= fetch_and_process_data()

        if request.method == 'POST':
            # Extract filter inputs
            fromMonth = request.POST.get('fromMonth')
            fromYear = request.POST.get('fromYear')
            toMonth = request.POST.get('toMonth')
            toYear = request.POST.get('toYear')
            selected_country = request.POST.getlist('country')
            selected_regulatory = request.POST.getlist('regulatory')
            selected_case_number = request.POST.getlist('case')
            selected_jurisdiction_body = request.POST.getlist('juri')
            # Filter by date range
            try:
                filtered_data = filter_by_date_range(filetrData, fromMonth, fromYear, toMonth, toYear)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)

            # Apply additional filters
            filtered_data = apply_filters(
                filtered_data, selected_country, selected_regulatory,selected_case_number,selected_jurisdiction_body
            )
            filtered_data = sorted(filtered_data, key=lambda x: getattr(x, 'Date', datetime.min),reverse=True)
            
            return render(request, 'insolvency/insolvencyFilter.html', {
                
                'data': filtered_data,  # Adjust pagination if necessary
                    'lenData':filetrData,
                    'rangedate': rangedate,
                    'country': sorted(country),
                'regulatory': sorted(regulatory),
                'Jurisdiction_Body': sorted(Jurisdiction_Body),
                'Case_Number': sorted(Case_Number),
                    'countryData': selected_country,
                    'regulatoryData': selected_regulatory,
                    'caseData': selected_case_number,
                    'juriData': selected_jurisdiction_body,
                    'cuntryLen':cuntryLen,
                'regLen':regLen,
                        
            })
        # return render(request, 'your_template.html', {"filtered_data": filetrData})
    except Exception as e:
        print(f"Error in filterData: {e}")
        return render(request, 'error.html', {"message": "An error occurred while processing data."})

@login_required
def findInsolCountry(request,cntry):
    findcountry=cntry
    filetrData, rangedate, country, regulatory, cuntryLen, regLen, Jurisdiction_Body, Case_Number= fetch_and_process_data()

    contryData=[]
    for i in filetrData:
        if i.rbCountry == findcountry:
            contryData.append(i) 
 
    return render(request, 'insolvency/insolCountryRagPage.html', {
                
                'data': contryData,  # Adjust pagination if necessary
                    'lenData':filetrData,
                    'rangedate': rangedate,
                    'country': sorted(country),
                'regulatory': sorted(regulatory),
                'Jurisdiction_Body': sorted(Jurisdiction_Body),
                'Case_Number': sorted(Case_Number),
                'cuntryLen':cuntryLen,
                'regLen':regLen,
                'countryName':findcountry
            })

@login_required
def findInsolReg(request,reg):
    findreg=reg
    filetrData, rangedate, country, regulatory, cuntryLen, regLen,Jurisdiction_Body, Case_Number = fetch_and_process_data()
    
    regData=[]
    for i in filetrData:
        if i.Regulatory == findreg:
            regData.append(i)
        
    return render(request, 'insolvency/insolCountryRagPage.html', {
                
                'data': regData,  # Adjust pagination if necessary
                    'lenData':filetrData,
                    'rangedate': rangedate,
                    'country': sorted(country),
                'regulatory': sorted(regulatory),
                'Jurisdiction_Body': sorted(Jurisdiction_Body),
                'Case_Number': sorted(Case_Number),
                'cuntryLen':cuntryLen,
                'regLen':regLen,
                'countryName':findreg
            })

