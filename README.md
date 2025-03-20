# TeamViewer-USM-Anywhere  
A script to collect logs from **TeamViewer** and send them to **USM Anywhere OXDR/SIEM via Syslog**.  

---

## Datasource  
[**TeamViewer**](https://www.teamviewer.com/en/products/teamviewer/) is a **remote control and access software** that allows users to connect to devices securely over the internet.  

### API Documentation  
For more details on the API, refer to the official **[TeamViewer API Documentation](https://webapi.teamviewer.com/api/v1/docs/index#/EventLogging)**.  

---

## How to Run the Script  

1. **Configure the script**  
   - Enter your **TeamViewer API Key** and **Sensor IP** into the `Teamviewer-config.json` file.  

2. **Set up log collection time**  
   - Update the **dates** in the configuration to ensure you only collect **recent logs** and avoid fetching excessive historical data.  

3. **Schedule the script**  
   - Create a **cron job** (Linux/macOS) or a **scheduled task** (Windows) to run the script at a defined interval, such as **every 30 minutes**.  
