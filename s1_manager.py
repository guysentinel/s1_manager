import tkinter as tk
import csv
import json
import asyncio
import aiohttp
import tkcalendar
import os
from xlsxwriter.workbook import Workbook
import requests
from functools import partial
import tkinter.filedialog
import logging
import tkinter.scrolledtext as ScrolledText
import datetime
import time


# Consts
window = tk.Tk()
window.title("S1 Manager")
window.minsize(800,800)
window.iconbitmap("s1-favicon-big.ico")
loginMenuFrame = tk.Frame()
mainMenuFrame = tk.Frame()
exportFromDVFrame = tk.Frame()
upgradeFromCSVFrame = tk.Frame()
exportActivityLogFrame = tk.Frame()
moveAgentsFrame = tk.Frame()
assignCustomerIdentifierFrame = tk.Frame()
decomissionAgentsFrame = tk.Frame()
error = tk.StringVar()
hostname = tk.StringVar()
apitoken = tk.StringVar()
proxy = tk.StringVar()
inputcsv = tk.StringVar()



class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

def testLogin(hostname,apitoken,proxy):
    headers = {
        "Content-type": "application/json",
        "Authorization": "ApiToken " + apitoken }
    r = requests.get(hostname + "/web/api/v2.1/system/info", headers=headers, proxies={'http' : proxy})
    if (r.status_code == 200):
        return True
    else:
        return False

def login():
    hostname.set(consoleAddressEntry.get())
    apitoken.set(apikTokenEntry.get())
    proxy.set(proxyEntry.get())
    if (testLogin(hostname.get(), apitoken.get(), proxy.get())):
        loginMenuFrame.pack_forget()
        mainMenuFrame.pack()
    else:
        tk.Label(master=loginMenuFrame, text="Login to the management console failed. Please check your credentials and try again", fg="red").grid(row=9, column=0, columnspan = 2, pady = 10)

def goBacktoMainPage():
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children():
            _list.extend(item.winfo_children())
    for item in _list:
        if isinstance(item,tkinter.Toplevel) is not True:
            item.pack_forget()
    mainMenuFrame.pack()

def switchFrames(framename):
    mainMenuFrame.pack_forget()
    framename.pack()

def exportFromDV():
    async def dv_query_to_csv(querytype, session, hostname, dv_query_id, headers, firstrun, proxy):
        params = '/web/api/v2.1/dv/events/' + querytype + '?queryId=' + dv_query_id
        url = hostname + params
        while url:
            async with session.get(url, headers=headers, proxy=proxy) as response:
                if response.status != 200:
                    error = 'Status: ' + str(response.status) + ' Problem with the request. Exiting.'
                    tk.Label(master=exportFromDVFrame, text=error, fg="red").grid(
                        row=6, column=0, pady=2)
                else:
                    data = await (response.json())
                    cursor = data['pagination']['nextCursor']
                    data = data['data']
                    if data:
                        for data in data:
                            if querytype == 'file':
                                f = csv.writer(open("dv_file.csv", "a+", newline='', encoding='utf-8'))
                                if firstrun:
                                    tmp = []
                                    for key, value in data.items():
                                        tmp.append(key)
                                    f.writerow(tmp)
                                    firstrun = False
                                tmp = []
                                for key, value in data.items():
                                    tmp.append(value)
                                f.writerow(tmp)

                            elif querytype == 'ip':
                                f = csv.writer(open("dv_ip.csv", "a+", newline='', encoding='utf-8'))
                                if firstrun:
                                    tmp = []
                                    for key, value in data.items():
                                        tmp.append(key)
                                    f.writerow(tmp)
                                    firstrun = False
                                tmp = []
                                for key, value in data.items():
                                    tmp.append(value)
                                f.writerow(tmp)

                            elif querytype == 'url':
                                f = csv.writer(open("dv_url.csv", "a+", newline='', encoding='utf-8'))
                                if firstrun:
                                    tmp = []
                                    for key, value in data.items():
                                        tmp.append(key)
                                    f.writerow(tmp)
                                    firstrun = False
                                tmp = []
                                for key, value in data.items():
                                    tmp.append(value)
                                f.writerow(tmp)

                            elif querytype == 'dns':
                                f = csv.writer(open("dv_dns.csv", "a+", newline='', encoding='utf-8'))
                                if firstrun:
                                    tmp = []
                                    for key, value in data.items():
                                        tmp.append(key)
                                    f.writerow(tmp)
                                    firstrun = False
                                tmp = []
                                for key, value in data.items():
                                    tmp.append(value)
                                f.writerow(tmp)

                            elif querytype == 'process':
                                f = csv.writer(open("dv_process.csv", "a+", newline='', encoding='utf-8'))
                                if firstrun:
                                    tmp = []
                                    for key, value in data.items():
                                        tmp.append(key)
                                    f.writerow(tmp)
                                    firstrun = False
                                tmp = []
                                for key, value in data.items():
                                    tmp.append(value)
                                f.writerow(tmp)

                            elif querytype == "registry":
                                f = csv.writer(open("dv_registry.csv", "a+", newline='', encoding='utf-8'))
                                if firstrun:
                                    tmp = []
                                    for key, value in data.items():
                                        tmp.append(key)
                                    f.writerow(tmp)
                                    firstrun = False
                                tmp = []
                                for key, value in data.items():
                                    tmp.append(value)
                                f.writerow(tmp)

                            elif querytype == "scheduled_task":
                                f = csv.writer(open("dv_scheduled_task.csv", "a+", newline='', encoding='utf-8'))
                                if firstrun:
                                    tmp = []
                                    for key, value in data.items():
                                        tmp.append(key)
                                    f.writerow(tmp)
                                    firstrun = False
                                tmp = []
                                for key, value in data.items():
                                    tmp.append(value)
                                f.writerow(tmp)
                    if cursor:
                        paramsnext = '/web/api/v2.1/dv/events/' + querytype + '?cursor=' + cursor + '&queryId=' + dv_query_id + '&limit=100'
                        url = hostname + paramsnext
                    else:
                        url = None

    async def run(hostname, dv_query_id, apitoken, proxy):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Content-type": "application/json",
                "Authorization": "ApiToken " + apitoken}
            for query in dv_query_id:
                firstrun = False
                if query == dv_query_id[0]:
                    firstrun = True
                typefile = asyncio.create_task(dv_query_to_csv('file', session, hostname, query, headers, firstrun, proxy))
                typeip = asyncio.create_task(dv_query_to_csv('ip', session, hostname, query, headers, firstrun, proxy))
                typeurl = asyncio.create_task(dv_query_to_csv('url', session, hostname, query, headers, firstrun, proxy))
                typedns = asyncio.create_task(dv_query_to_csv('dns', session, hostname, query, headers, firstrun, proxy))
                typeprocess = asyncio.create_task(
                    dv_query_to_csv('process', session, hostname, query, headers, firstrun, proxy))
                typeregistry = asyncio.create_task(
                    dv_query_to_csv('registry', session, hostname, query, headers, firstrun, proxy))
                typescheduledtask = asyncio.create_task(
                    dv_query_to_csv('scheduled_task', session, hostname, query, headers, firstrun, proxy))
                await typefile
                await typeip
                await typeurl
                await typedns
                await typeprocess
                await typeregistry
                await typescheduledtask

    dv_query_id = queryIdEntry.get()
    if dv_query_id:
        dv_query_id = dv_query_id.split(',')
        asyncio.run(run(hostname.get(), dv_query_id, apitoken.get(), proxy.get()))
        filename = "-"
        filename = filename.join(dv_query_id)
        workbook = Workbook(filename + '.xlsx')
        csvs = ["dv_file.csv", "dv_ip.csv", "dv_url.csv", "dv_dns.csv", "dv_process.csv", "dv_registry.csv",
                "dv_scheduled_task.csv"]
        for csvfile in csvs:
            worksheet = workbook.add_worksheet(csvfile.split(".")[0])
            if os.path.isfile(csvfile):
                with open(csvfile, 'r', encoding="utf8") as f:
                    reader = csv.reader(f)
                    for r, row in enumerate(reader):
                        for c, col in enumerate(row):
                            worksheet.write(r, c, col)
                os.remove(csvfile)
        workbook.close()
        done = "Done! Created the file " + filename + ".xlsx"
        tk.Label(master=exportFromDVFrame, text=done, font=("Courier", 18)).grid(row=6, column=0, pady=2)
    else:
        tk.Label(master=exportFromDVFrame, text="No DV Query ID found. Please try again", fg="red").grid(row=5, column=0, pady= 2)

def exportActivityLog(searchOnly):
    st = ScrolledText.ScrolledText(master=exportActivityLogFrame, state='disabled')
    st.configure(font='TkFixedFont')
    st.grid(row=10, column=0, columnspan=3, pady=2)
    text_handler = TextHandler(st)
    logging.basicConfig(filename='activitylogexport.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.addHandler(text_handler)
    headers = {
        "Content-type": "application/json",
        "Authorization": "ApiToken " + apitoken.get()}
    os.environ['TZ'] = 'UTC'
    p = "%Y-%m-%d"
    fromdate_epoch = str(int(time.mktime(time.strptime(dateFrom.get(), p)))) + "000"
    todate_epoch = str(int(time.mktime(time.strptime(dateTo.get(), p)))) + "000"
    if dateFrom.get() and dateTo.get():
        url = hostname.get() + f'/web/api/v2.1/activities?limit=1000&createdAt__between={fromdate_epoch}-{todate_epoch}&countOnly=false&includeHidden=false'
        if searchOnly:
            while url:
                response = requests.get(url,headers=headers, proxies={'http' : proxy.get()})
                if response.status_code != 200:
                    logger.error('Status: ' + str(response.status_code) + ' Problem with the request. Details - ' + str(
                        response.text))
                else:
                    data = response.json()
                    cursor = data['pagination']['nextCursor']
                    data = data['data']
                    if data:
                        for item in data:
                            if stringSearchEntry.get().upper() in item["primaryDescription"].upper():
                                logger.info(f'{item["createdAt"]} - {item["primaryDescription"]} - {item["secondaryDescription"]}')
                            elif item["secondaryDescription"]:
                                if stringSearchEntry.get().upper() in item["secondaryDescription"].upper():
                                    logger.info(
                                        f'{item["createdAt"]} - {item["primaryDescription"]} - {item["secondaryDescription"]}')
                    if cursor:
                        paramsnext = f'/web/api/v2.1/activities?limit=1000&createdAt__between={fromdate_epoch}-{todate_epoch}&countOnly=false&cursor={cursor}&includeHidden=false'
                        url = hostname.get() + paramsnext
                    else:
                        url = None
        else:
            timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            f = csv.writer(open(f"activityLogExport{timestamp}.csv", "a+", newline='', encoding='utf-8'))
            firstrun = True
            while url:
                response = requests.get(url,headers=headers, proxies={'http' : proxy.get()})
                if response.status_code != 200:
                    logger.error('Status: ' + str(response.status_code) + ' Problem with the request. Details - ' + str(
                        response.text))
                else:
                    data = response.json()
                    cursor = data['pagination']['nextCursor']
                    data = data['data']
                    if data:
                        if firstrun:
                            tmp = []
                            for key, value in data[0].items():
                                tmp.append(key)
                            f.writerow(tmp)
                            firstrun = False
                        for item in data:
                            tmp = []
                            for key, value in item.items():
                                tmp.append(value)
                            f.writerow(tmp)
                    if cursor:
                        paramsnext = f'/web/api/v2.1/activities?limit=1000&createdAt__between={fromdate_epoch}-{todate_epoch}&countOnly=false&cursor={cursor}&includeHidden=false'
                        url = hostname.get() + paramsnext
                    else:
                        url = None
            logger.info(f"Done! Output file is - activityLogExport{timestamp}.csv")

    else:
        logger.error("You must state a FROM date and a TO date")


def upgradeFromCSV(justPackages):
    st = ScrolledText.ScrolledText(master=upgradeFromCSVFrame, state='disabled')
    st.configure(font='TkFixedFont')
    st.grid(row=9, column=0, columnspan=3, pady=2)
    text_handler = TextHandler(st)
    logging.basicConfig(filename='upgradefromcsv.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.addHandler(text_handler)
    headers = {
        "Content-type": "application/json",
        "Authorization": "ApiToken " + apitoken.get()}

    if justPackages:
        params = '/web/api/v2.1/update/agent/packages?sortBy=updatedAt&sortOrder=desc&countOnly=false&limit=1000'
        url = hostname.get() + params
        f = csv.writer(open("packages_list.csv", "a+", newline='', encoding='utf-8'))
        f.writerow(
            ['Name', 'ID', 'Version', 'OS Type', 'OS Arch', 'Package Type', 'File Extension', 'Status', 'Scope Level'])

        while url:
            response = requests.get(url, headers=headers, proxies={'http' : proxy.get()})
            if response.status_code != 200:
                logger.error('Status: ' + str(response.status_code) + ' Problem with the request. Details - ' + str(response.text))
            else:
                data = response.json()
                cursor = data['pagination']['nextCursor']
                data = data['data']
                if data:
                    for data in data:
                        f.writerow([
                            [data["fileName"]], data["id"], data["version"], data['osArch'], data["osType"],
                            data['packageType'], data['fileExtension'], data['status'], data['scopeLevel']
                        ])
                if cursor:
                    paramsnext = '/web/api/v2.1/update/agent/packages?sortBy=updatedAt&sortOrder=desc&limit=1000&cursor=' + cursor + '&countOnly=false'
                    url = hostname.get() + paramsnext
                else:
                    url = None
        logger.info("Printed packages list into packages_list.csv")
    else:
        with open(inputcsv.get()) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                logger.info(f'\t Upgrading endpoint named -  {row[0]}')
                url = hostname.get() + '/web/api/v2.1/agents/actions/update-software'
                body = {
                    "filter": {
                        "computerName": row[0]
                    },
                    "data": {
                        "packageId": packageIDEntry.get()
                    }
                }
                response = requests.post(url, data=json.dumps(body), headers=headers, proxies={'http' : proxy.get()})
                if response.status_code != 200:
                    logger.error('Failed to upgrade endpoint ' + row[0] + ' Error code: '
                          + str(response.status_code) + ' Description: ' + str(response.text))
                else:
                    data = response.json()
                    logger.info(f'Sent upgrade command to {data["data"]["affected"]} endpoints')
                line_count += 1
            logger.info(f'Finished! Processed {line_count} lines.')

def moveAgents(justGroups):
    st = ScrolledText.ScrolledText(master=moveAgentsFrame, state='disabled')
    st.configure(font='TkFixedFont')
    st.grid(row=7, column=0, columnspan=3, pady=2)
    text_handler = TextHandler(st)
    logging.basicConfig(filename='moveagentsfromcsv.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.addHandler(text_handler)
    headers = {
        "Content-type": "application/json",
        "Authorization": "ApiToken " + apitoken.get()}
    if justGroups:
        params = '/web/api/v2.0/groups?isDefault=false&limit=100&type=static&countOnly=false'
        url = hostname.get() + params
        f = csv.writer(open("group_to_id_map.csv", "a+", newline='', encoding='utf-8'))
        f.writerow(['Name', 'ID', 'Site ID', 'Created By'])
        while url:
            response = requests.get(url, headers=headers, proxies={'http' : proxy.get()})
            if response.status_code != 200:
                logger.error('Status: ' + str(response.status_code) + ' Problem with the request. Details - ' + str(response.text))
            else:
                data = response.json()
                cursor = data['pagination']['nextCursor']
                data = data['data']
                if data:
                    for data in data:
                        f.writerow([
                            [data["name"]], data["id"], data["siteId"], data["creator"]
                        ])
                if cursor:
                    paramsnext = '/web/api/v2.0/groups?isDefault=false&limit=100&type=static&cursor=' + cursor + '&countOnly=false'
                    url = hostname.get() + paramsnext
                else:
                    url = None
        logger.info("Added group mapping to the file group_to_id_map.csv ")
    else:
        with open(inputcsv.get()) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                logger.info(f'\t Moving endpoint name {row[0]} to group ID {row[1]}')
                url = hostname.get() + '/web/api/v2.0/groups/' + row[1] + '/move-agents'
                body = {
                    "filter": {
                        "computerName": row[0]
                    }
                }
                response = requests.put(url, data=json.dumps(body), headers=headers, proxies={'http' : proxy.get()})
                if response.status_code != 200:
                    logger.error('Failed to transfer endpoint ' + row[0] + ' to group ' + row[1] + ' Error code: '
                          + str(response.status_code) + ' Description: ' + str(response.text))
                else:
                    data = response.json()
                    logger.info(f'Moved {data["data"]["agentsMoved"]} endpoints')
                line_count += 1
            logger.info(f'Finished! Processed {line_count} lines.')


def assignCustomerIdentifier():
    st = ScrolledText.ScrolledText(master=assignCustomerIdentifierFrame, state='disabled')
    st.configure(font='TkFixedFont')
    st.grid(row=8, column=0, columnspan=3, pady=2)
    text_handler = TextHandler(st)
    logging.basicConfig(filename='upgradefromcsv.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.addHandler(text_handler)
    headers = {
        "Content-type": "application/json",
        "Authorization": "ApiToken " + apitoken.get()}
    with open(inputcsv.get()) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            logger.info(f'\t Updating customer identifier for endpoint -  {row[0]}')
            url = hostname.get() + '/web/api/v2.1/agents/actions/set-external-id'
            body = {
                    "filter": {
                        "computerName": row[0]
                    },
                    "data": {
                        "externalId": customerIdentifierEntry.get()
                    }
                }
            response = requests.post(url, data=json.dumps(body), headers=headers, proxies={'http' : proxy.get()})
            if response.status_code != 200:
                logger.error('Failed to update customer identifier for endpoint ' + row[0] + ' Error code: '
                      + str(response.status_code) + ' Description: ' + str(response.text))
            else:
                r = response.json()
                affected_num_of_endpoints = r['data']['affected']
                if (affected_num_of_endpoints < 1):
                    logger.info(f'No endpoint matched the name {row[0]}')
                elif (affected_num_of_endpoints > 1):
                    logger.info(f'{affected_num_of_endpoints} endpoints matched the name {row[0]} , customer identifier was updated for all')
                else:
                    logger.info(f'Successfully updated the customer identifier')
            line_count += 1
        logger.info(f'Finished! Processed {line_count} lines.')


def decomissionAgents():
    st = ScrolledText.ScrolledText(master=decomissionAgentsFrame, state='disabled')
    st.configure(font='TkFixedFont')
    st.grid(row=6, column=0, columnspan=3, pady=2)
    text_handler = TextHandler(st)
    logging.basicConfig(filename='decomissionagentfromcsv.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.addHandler(text_handler)
    headers = {
        "Content-type": "application/json",
        "Authorization": "ApiToken " + apitoken.get()}
    with open(inputcsv.get()) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            logger.info(f'\t Decomissioning Endpoint -  {row[0]}')
            logger.info(f'Getting endpoint ID for {row[0]}')
            url = hostname.get() + f'/web/api/v2.1/agents?countOnly=false&computerName={row[0]}&limit=1000'
            response = requests.get(url, headers=headers, proxies={'http' : proxy.get()})
            if response.status_code != 200:
                logger.error('Failed to get ID for endpoint ' + row[0] + ' Error code: '
                      + str(response.status_code) + ' Description: ' + str(response.text))
            else:
                r = response.json()
                totalitems = r['pagination']['totalItems']
                if (totalitems < 1):
                    logger.info(f"Could not locate any IDs for endpoint named {row[0]} - Please note the query is CaSe SenSiTiVe")
                else:
                    r = r['data']
                    uuidslist = []
                    for item in r:
                        uuidslist.append(item['id'])
                        logger.info(f"Found ID {item['id']}! adding it for decomissining")
                    url = hostname.get() + '/web/api/v2.1/agents/actions/decommission'
                    body = {
                            "filter": {
                                "ids": uuidslist
                            }
                        }
                    response = requests.post(url, data=json.dumps(body), headers=headers, proxies={'http' : proxy.get()})
                    if response.status_code != 200:
                        logger.error('Failed to decomission endpoint ' + row[0] + ' Error code: '
                              + str(response.status_code) + ' Description: ' + str(response.text))
                    else:
                        r = response.json()
                        affected_num_of_endpoints = r['data']['affected']
                        if (affected_num_of_endpoints < 1):
                            logger.info(f'No endpoint matched the name {row[0]}')
                        elif (affected_num_of_endpoints > 1):
                            logger.info(f'{affected_num_of_endpoints} endpoints matched the name {row[0]} , all of them got decomissioned')
                        else:
                            logger.info(f'Successfully decomissioned the endpoint')
            line_count += 1
        logger.info(f'Finished! Processed {line_count} lines.')

def selectCSVFile():
    file = tkinter.filedialog.askopenfilename()
    inputcsv.set(file)

# Login Menu Frame
consoleAddressLabel = tk.Label(master=loginMenuFrame, text="Insert the full URL of the management console i.e https://usea1-100.sentinelone.net")
consoleAddressEntry = tk.Entry(master=loginMenuFrame, width=80)
apikTokenLabel = tk.Label(master=loginMenuFrame, text="Insert your API Token. See the API Documentation for more information on how to generate it")
apikTokenEntry = tk.Entry(master=loginMenuFrame, width=80)
proxyLabel = tk.Label(master=loginMenuFrame, text="Insert Proxy details i.e http://username:password@proxy.com - If not used, keep Blank")
proxyEntry = tk.Entry(master=loginMenuFrame, width=80)
submitButton = tk.Button(master=loginMenuFrame, text="Submit", font=("Courier", 22), command=login)
tk.Label(master=loginMenuFrame, text="Login",font=("Courier", 44)).grid(row=0, column=0, columnspan = 2, pady = 20)
consoleAddressLabel.grid(row=1, column=0, pady=2)
consoleAddressEntry.grid(row=2, column=0, pady=2)
apikTokenLabel.grid(row=3, column=0, pady=2)
apikTokenEntry.grid(row=4, column=0, pady=2)
proxyLabel.grid(row=5, column=0, pady=2)
proxyEntry.grid(row=6, column=0, pady=2)
submitButton.grid(row=7, column=0, columnspan=2, pady=10)
loginMenuFrame.pack()

# Main Menu Frame
logo = r"""
 ▄▄▄▄▄▄▄▄▄▄▄     ▄▄▄▄           ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌  ▄█░░░░▌         ▐░░▌     ▐░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀  ▐░░▌▐░░▌         ▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌
▐░▌            ▀▀ ▐░░▌         ▐░▌▐░▌ ▐░▌▐░▌▐░▌       ▐░▌▐░▌▐░▌    ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌       ▐░▌
▐░█▄▄▄▄▄▄▄▄▄      ▐░░▌         ▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▌   ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌     ▐░░▌         ▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░▌▐░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀█░▌     ▐░░▌         ▐░▌   ▀   ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌   ▐░▌ ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌ ▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀█░█▀▀ 
          ▐░▌     ▐░░▌         ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌    ▐░▌▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌     ▐░▌  
 ▄▄▄▄▄▄▄▄▄█░▌ ▄▄▄▄█░░█▄▄▄      ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌     ▐░▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌      ▐░▌ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌      ▐░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀         ▀  ▀         ▀  ▀        ▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀ """
tk.Label(master=mainMenuFrame, text=logo, justify=tk.LEFT, font="TkFixedFont").grid(row=0, column=0, columnspan = 3, pady = 20)
tk.Button(master=mainMenuFrame, text="Export events from Deep Visiblity", command=partial(switchFrames,exportFromDVFrame)).grid(row=1, column=0, pady=10)
tk.Button(master=mainMenuFrame, text="Export and Search Activity Log", command=partial(switchFrames,exportActivityLogFrame)).grid(row=1, column=1, pady=10)
tk.Button(master=mainMenuFrame, text="Upgrade Agents from CSV", command=partial(switchFrames,upgradeFromCSVFrame)).grid(row=1, column=2, pady=10)
tk.Button(master=mainMenuFrame, text="Move Agents between Groups from CSV", command=partial(switchFrames, moveAgentsFrame)).grid(row=2, column=0, pady=10)
tk.Button(master=mainMenuFrame, text="Assign Customer Identifier from CSV", command=partial(switchFrames,assignCustomerIdentifierFrame)).grid(row=2, column=1, pady=10)
tk.Button(master=mainMenuFrame, text="Decomission Agents from CSV", command=partial(switchFrames,decomissionAgentsFrame)).grid(row=2, column=2, pady=10)
tk.Label(master=mainMenuFrame, text="Version: Kauai", font=("Courier", 10)).grid(row=3, column=1, pady=10)

# Export from DV Frame
tk.Label(master=exportFromDVFrame, text="Export Deep Visiblity Events to CSV",font=("Courier", 44)).grid(row=0, column=0, columnspan = 2, pady = 20)
tk.Label(master=exportFromDVFrame, text="Insert Deep Visiblity Query ID (i.e stream6a...123) \n If you have more than 20K results, you can concat several smaller queries seperated by comma (i.e stream9a...123,stream2b...129,stream8s...145)", font=("Courier", 10)).grid(row=1, column=0, pady= 2)
queryIdEntry = tk.Entry(master=exportFromDVFrame, width=80)
queryIdEntry.grid(row=2, column=0, pady= 2)
tk.Button(master=exportFromDVFrame, text="Submit (this might take awhile)", font=("Courier", 22), command=exportFromDV).grid(row=3, column=0, pady= 2)
tk.Button(master=exportFromDVFrame, text="Back to Main Menu", font=("Courier", 22), command=goBacktoMainPage).grid(row=4, column=0, pady= 2)

# Upgrade from CSV Frame
tk.Label(master=upgradeFromCSVFrame, text="Upgrade Agents from CSV en masse",font=("Courier", 44)).grid(row=0, column=0, columnspan = 2, pady = 20)
tk.Button(master=upgradeFromCSVFrame, text="Export Packages List (to get the relevant Package ID)", font=("Courier", 15), command=partial(upgradeFromCSV, True)).grid(row=1, column=0, pady= 2)
tk.Label(master=upgradeFromCSVFrame, text="Insert the Package ID", font=("Courier", 12)).grid(row=2, column=0, pady= 2)
packageIDEntry = tk.Entry(master=upgradeFromCSVFrame, width=80)
packageIDEntry.grid(row=3, column=0, pady= 2)
tk.Label(master=upgradeFromCSVFrame, text="Select a CSV file containing a single column with a named list of endpoints to upgrade", font=("Courier", 12)).grid(row=4, column=0, pady= 2)
tk.Button(master=upgradeFromCSVFrame, text="Browse", font=("Courier", 15), command=selectCSVFile).grid(row=5, column=0, pady= 2)
tk.Label(master=upgradeFromCSVFrame, textvariable=inputcsv).grid(row=6, column=0, pady= 2)
tk.Button(master=upgradeFromCSVFrame, text="Submit (this might take awhile)", font=("Courier", 22), command=partial(upgradeFromCSV, False)).grid(row=7, column=0, pady= 2)
tk.Button(master=upgradeFromCSVFrame, text="Back to Main Menu", font=("Courier", 22), command=goBacktoMainPage).grid(row=8, column=0, pady= 2)

# Move agents between groups from CSV Frame
tk.Label(master=moveAgentsFrame, text="Move Agents between Groups from CSV",font=("Courier", 44)).grid(row=0, column=0, columnspan = 2, pady = 20)
tk.Button(master=moveAgentsFrame, text="Export Groups List (to get the relevant Group ID)", font=("Courier", 15), command=partial(moveAgents, True)).grid(row=1, column=0, pady= 2)
tk.Label(master=moveAgentsFrame, text="Select a CSV file containing two columns with endpoints names and target group IDs", font=("Courier", 12)).grid(row=2, column=0, pady= 2)
tk.Button(master=moveAgentsFrame, text="Browse", font=("Courier", 15), command=selectCSVFile).grid(row=3, column=0, pady= 2)
tk.Label(master=moveAgentsFrame, textvariable=inputcsv).grid(row=4, column=0, pady= 2)
tk.Button(master=moveAgentsFrame, text="Submit (this might take awhile)", font=("Courier", 22), command=partial(moveAgents, False)).grid(row=5, column=0, pady= 2)
tk.Button(master=moveAgentsFrame, text="Back to Main Menu", font=("Courier", 22), command=goBacktoMainPage).grid(row=6, column=0, pady= 2)


# Assign Customer Identifier from CSV Frame
tk.Label(master=assignCustomerIdentifierFrame, text="Assign Customer Identifier from CSV",font=("Courier", 44)).grid(row=0, column=0, columnspan = 2, pady = 20)
tk.Label(master=assignCustomerIdentifierFrame, text="Insert the Customer Identifier", font=("Courier", 12)).grid(row=1, column=0, pady= 2)
customerIdentifierEntry = tk.Entry(master=assignCustomerIdentifierFrame, width=80)
customerIdentifierEntry.grid(row=2, column=0, pady= 2)
tk.Label(master=assignCustomerIdentifierFrame, text="Select a CSV file containing a single column with endpoint names", font=("Courier", 12)).grid(row=3, column=0, pady= 2)
tk.Button(master=assignCustomerIdentifierFrame, text="Browse", font=("Courier", 15), command=selectCSVFile).grid(row=4, column=0, pady= 2)
tk.Label(master=assignCustomerIdentifierFrame, textvariable=inputcsv).grid(row=5, column=0, pady= 2)
tk.Button(master=assignCustomerIdentifierFrame, text="Submit (this might take awhile)", font=("Courier", 22), command=assignCustomerIdentifier).grid(row=6, column=0, pady= 2)
tk.Button(master=assignCustomerIdentifierFrame, text="Back to Main Menu", font=("Courier", 22), command=goBacktoMainPage).grid(row=7, column=0, pady= 2)


# Decomission Agents from CSV Frame
tk.Label(master=decomissionAgentsFrame, text="Decomission Agents from CSV",font=("Courier", 44)).grid(row=0, column=0, columnspan = 2, pady = 20)
tk.Label(master=decomissionAgentsFrame, text="Select a CSV file containing a single column of endpoint names to be decomissioned", font=("Courier", 12)).grid(row=1, column=0, pady= 2)
tk.Button(master=decomissionAgentsFrame, text="Browse", font=("Courier", 15), command=selectCSVFile).grid(row=2, column=0, pady= 2)
tk.Label(master=decomissionAgentsFrame, textvariable=inputcsv).grid(row=3, column=0, pady= 2)
tk.Button(master=decomissionAgentsFrame, text="Submit (this might take awhile)", font=("Courier", 22), command=decomissionAgents).grid(row=4, column=0, pady= 2)
tk.Button(master=decomissionAgentsFrame, text="Back to Main Menu", font=("Courier", 22), command=goBacktoMainPage).grid(row=5, column=0, pady= 2)


# Export and Search Activity Log Frame
tk.Label(master=exportActivityLogFrame, text="Export and Search Activity Log",font=("Courier", 44)).grid(row=0, column=0, columnspan = 2, pady = 20)
tk.Label(master=exportActivityLogFrame, text="Choose a FROM date").grid(row=1, column=0, pady =2)
dateFrom = tkcalendar.DateEntry(master=exportActivityLogFrame, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='yyyy-MM-dd')
dateFrom.grid(row=2, column=0, pady=2)
tk.Label(master=exportActivityLogFrame, text="Choose a TO date").grid(row=3, column=0, pady =2)
dateTo = tkcalendar.DateEntry(master=exportActivityLogFrame, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='yyyy-MM-dd')
dateTo.grid(row=4, column=0, pady=2)
tk.Label(master=exportActivityLogFrame, text="Search a string", font=("Courier", 15)).grid(row=5, column=0, pady= 2)
stringSearchEntry = tk.Entry(master=exportActivityLogFrame, width=80)
stringSearchEntry.grid(row=6, column=0, pady= 2)
tk.Button(master=exportActivityLogFrame, text="Search (this might take awhile)", font=("Courier", 15), command=partial(exportActivityLog, True)).grid(row=7, column=0, pady= 2)
tk.Button(master=exportActivityLogFrame, text="Export Entire Activity Log to CSV (this might take awhile)", font=("Courier", 15), command=partial(exportActivityLog, False)).grid(row=8, column=0, pady= 2)
tk.Button(master=exportActivityLogFrame, text="Back to Main Menu", font=("Courier", 22), command=goBacktoMainPage).grid(row=9, column=0, pady= 2)



window.mainloop()