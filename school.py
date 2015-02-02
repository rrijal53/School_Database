import urllib2
import re
from lxml import html
def school_type(school_report):
    import cStringIO
    from lxml import etree
    from BeautifulSoup import BeautifulSoup
    import urllib2
    import re
    from lxml import html
    school_type_row = ["ECD","Primary","Lower_Secondary","Secondary","Higher_Secondary"]
    school_type_column = ["Community (Aided)", "Community Managed", "Community (Teacher Aid)", "Community (Unaided)", "Institutional (Private Trust)", "Institutional (Public Trust)", "Institutional (Enlisted with Company)", "Madrassa", "Gumba", "Ashram", "Community ECD"]
    soup = BeautifulSoup(school_report)
    f = cStringIO.StringIO(soup.prettify())
    parser = etree.XMLParser(resolve_entities=False, recover=True)
    tree = etree.parse(f,parser=parser)
    find_text = etree.XPath("//img[@src='images/tick.gif']")

    xpath = tree.getpath(find_text(tree)[len(find_text(tree))-1].getparent())
    values = re.findall(r'\d+', xpath)[-2:]
    if school_type_row[int(values[1])-2]=="ECD":
		return school_type_column[int(values[0])-3]+"####"
    elif school_type_row[int(values[1])-2]=="Primary":
		return "#"+school_type_column[int(values[0])-3]+"###"
    elif school_type_row[int(values[1])-2]=="Lower_Secondary":
		return "##"+school_type_column[int(values[0])-3]+"##"
    elif school_type_row[int(values[1])-2]=="Secondary":
		return "###"+school_type_column[int(values[0])-3]+"#"
    else:
    		return "####"+school_type_column[int(values[0])-3]

years = {2070,2069,2068,2067,2066,2065,2064}
school_type_row = {"ECD","Primary","Lower_Secondary","Secondary","Higher_Secondary"}
school_type_column = {"Community (Aided)", "Community Managed", "Community (Teacher Aid)", "Community (Unaided)", "Institutional (Private Trust)", "Institutional (Public Trust)", "Institutional (Enlisted with Company)", "Madrassa", "Gumba", "Ashram", "Community ECD"}

district_list = urllib2.urlopen("http://202.70.77.75:8080/flash/schoolreport/reportprebe.php?req=distlist").read()
district_list = district_list.replace('District: <select name="d" id="d" onchange="return handlechange(this, event);"><option value="">- Select District -</option>',"").replace("</select>","")
district_list = district_list.split("</option>")
f=open("School_data.txt",'w')
f.write("Year#school_code#school_name#development_region#eco_belt#zone#District#VDC#Address#Ward_No#ECD#PRIMARY#LOWER_SECONDARY#SECONDARY#HIGHER_SECONDARY"+'\n')
for d in district_list:
    district_code = re.sub('<option value="',"",d)[0:2]
    district_name = re.sub(r'<option value="\d+">',"",d)
    vdc_list = urllib2.urlopen("http://202.70.77.75:8080/flash/schoolreport/reportprebe.php?req=vdclist&distcode="+district_code).read()
    vdc_list = vdc_list.replace('VDC: <select name="v" id="v" onchange="return handlechange(this, event);"><option value="">- All Schools -</option>','')
    vdc_list =  vdc_list.replace('</select>','')
    vdc_list = vdc_list.split("</option>")
    for v in vdc_list:
        vdc_code = re.sub('<option value="',"",v)[0:3]
        vdc_name = re.sub(r'<option value="\d+">',"",v)
        school_list = urllib2.urlopen("http://202.70.77.75:8080/flash/schoolreport/reportprebe.php?req=schoollist&distcode="+district_code+"&vdccode="+vdc_code+"&y=2070").read()
        school_list = school_list.replace('School: <select name="s" id="s"><option value="">- All Schools -</option>','')
        school_list =  school_list.replace('</select>','')
        school_list = school_list.split("</option>")
        for s in school_list:
            school_code = re.sub("<option value='","",s)[0:9]
            school_name = re.sub(r"<option value='\d+'>","",s)
            for y in years:
                try:
                    school_report = urllib2.urlopen("http://202.70.77.75:8080/flash/schoolreport/reportshow.php?d="+district_code+"&v="+vdc_code+"&s="+school_code+"&t=&yr="+str(y)).read()
                    sub_root = html.fromstring(school_report)
                    development_region = sub_root.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[2]/td[2]/text()')[0].strip()
                    eco_belt =  sub_root.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[3]/td[2]/text()')[0].strip()
                    zone = sub_root.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[4]/td[2]/text()')[0].strip()
		    District = sub_root.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[5]/td[2]/text()')[0].strip()
                    VDC = sub_root.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[6]/td[2]/text()')[0].strip()
                    Address = sub_root.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[7]/td[2]/text()')[0].strip()
                    Ward_No = sub_root.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[8]/td[2]/text()')[0].strip()
		    print y
		    f.write(str(y)+"#"+school_code+"#"+school_name+"#"+development_region+"#"+eco_belt+"#"+zone+"#"+District+"#"+VDC+"#"+Address+"#"+Ward_No+"#"+school_type(school_report)+"\n")
                    print school_type(school_report)
                except:
                    continue
                
                

        
    
