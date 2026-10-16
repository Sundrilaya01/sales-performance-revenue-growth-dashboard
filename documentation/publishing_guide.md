# Power BI Service Deployment & Publishing Guide

**Project:** Sales Performance & Revenue Growth Dashboard  
**Phase:** Phase 8 — Publishing Guidance and Portfolio Preparation  
**Role:** Senior BI Delivery Engineer & Technical Documentation Specialist  
**Target Environment:** Power BI Service (SaaS Cloud / Fabric Capacity)  

---

## 1. Overview
This guide provides step-by-step instructions for publishing, configuring, scheduling, and securing the **Sales Performance & Revenue Growth Dashboard** in Microsoft Power BI Service.

> [!NOTE]
> Specific Microsoft 365 tenant licenses, workspace administrative privileges, and Azure Active Directory tenant IDs vary per organization. Confirm your account entitlements with your enterprise Power BI administrator before deployment.

---

## 2. Pre-Publishing Verification Checklist
Before initiating the publishing workflow:
- [ ] Ingest all 6 processed CSV tables from `data/processed/` via Power Query.
- [ ] Confirm the 5 relationships are active and configured as **Single-direction 1-to-many (`1:*`)**.
- [ ] Set `dim_date[month_name]` to Sort by `month_number` and `dim_date[month_year]` to Sort by `year_month_sort`.
- [ ] Mark `dim_date` as the official **Date Table**.
- [ ] Verify all 11 explicit DAX measures from `scripts/dax_measures.dax` exist in the `_Measures` table.
- [ ] Import and apply `scripts/powerbi_theme.json`.
- [ ] Save the local file as `Sales Performance & Revenue Growth Dashboard.pbix`.

---

## 3. Publishing Workflow (Step-by-Step)

### Step 1: Save and Publish from Power BI Desktop
1. In **Power BI Desktop**, click the **Home** ribbon.
2. Click **Publish** (or navigate to `File` -> `Publish` -> `Publish to Power BI`).
3. If prompted, sign in with your enterprise Microsoft 365 credentials (`user@company.com`).

### Step 2: Select the Destination Workspace
1. Select the designated organizational workspace (e.g., `Commercial Analytics — Production` or `Sales Operations`).
2. *Best Practice:* Never publish production dashboards directly to **My Workspace**; always publish to a dedicated collaborative workspace backed by Microsoft 365 Groups or Microsoft Fabric capacity.
3. Click **Select**. Power BI Desktop will upload the report canvas and semantic model.
4. Once completed, a confirmation dialog will display: *"Publishing succeeded. Open 'Sales Performance & Revenue Growth Dashboard.pbix' in Power BI"*.

---

## 4. Post-Publishing Configuration in Power BI Service

### Step 4.1: Configure Data Source Credentials
1. Open [app.powerbi.com](https://app.powerbi.com) and navigate to the target workspace.
2. Locate the **Semantic Model** titled `Sales Performance & Revenue Growth Dashboard`.
3. Click the three dots (`...`) -> select **Settings**.
4. Expand **Data source credentials**:
   - For cloud-stored data (Azure Blob, OneDrive, SharePoint): Select **OAuth2** authentication with **Organizational** privacy level.
   - For on-premises file paths (e.g., local server drives): Configure gateway access (see Section 4.2 below) and enter Windows authentication credentials.

### Step 4.2: Configure On-Premises Data Gateway (If Using Local Storage)
*When reading data from on-premises drives or local server network paths:*
1. Install and register the **Power BI On-Premises Data Gateway** (Standard Mode recommended for multi-user production environments).
2. In Power BI Service Settings -> **Gateway connections**:
   - Enable the toggle **Use an on-premises data gateway**.
   - Map the CSV folder path `D:\Power BI\Sales Performance & Revenue Growth Dashboard\data\processed\` to the registered gateway cluster.
3. Verify connection status displays a green checkmark: *"Online / Connected"*.

### Step 4.3: Configure Automated Scheduled Refresh
1. In Semantic Model Settings, expand **Scheduled refresh**.
2. Toggle **Keep your data fresh** to **On**.
3. **Refresh Frequency:** Select **Daily** (or **Weekly**).
4. **Time Zone:** Select your organization's primary operating time zone (e.g., `(UTC-05:00) Eastern Time (US & Canada)`).
5. **Time Slots:** Add scheduled execution times (e.g., `06:00 AM` and `01:00 PM` to precede morning executive briefings).
6. **Failure Notifications:** Check **Send refresh failure notification emails to the semantic model owner** and add any operational monitoring distribution lists.
7. Click **Apply**.

---

## 5. Security & Access Governance

### 5.1 Row-Level Security (RLS) Implementation
To restrict Regional Sales Managers to their respective territories while granting global visibility to executive leadership:

1. **Define Roles in Power BI Desktop:**
   - In Power BI Desktop, navigate to **Modeling** ribbon -> click **Manage roles**.
   - Create a role named `Regional_Sales_Manager`.
   - On table `dim_regions`, enter the DAX filter expression:
     ```dax
     [region_name] = LOOKUPVALUE(
         dim_sales_reps[assigned_region],
         dim_sales_reps[user_email],
         USERPRINCIPALNAME()
     )
     ```
   - Click **Save**.
2. **Assign Members in Power BI Service:**
   - In the workspace, click `...` on the Semantic Model -> select **Security**.
   - Select the `Regional_Sales_Manager` role.
   - Enter individual user email addresses or Microsoft 365 security groups (e.g., `SG-SalesManagers-East@company.com`).
   - Click **Add** -> **Save**.
   - Test roles using **Test as role** to verify visual filtering.

### 5.2 Workspace Access vs. App Distribution
* **Workspace Roles:**
  - **Admin / Member:** Core BI engineering team (create, edit, publish models).
  - **Contributor:** Business Analysts (create derivative reports from the semantic model).
  - **Viewer:** Read-only access to reports and dashboards within the workspace.
* **App Distribution (Recommended for End Users):**
  - Click **Create app** in the workspace header.
  - Package the Executive Sales Overview into a branded Power BI App.
  - Grant access to the `Commercial-Leadership` security group.
  - End users consume reports via the streamlined App interface without risk of altering underlying models or configurations.

---

## 6. Official Microsoft Reference Documentation
- [Publish from Power BI Desktop](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-upload-desktop-files)
- [Configure Scheduled Refresh in Power BI](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-scheduled-refresh)
- [Manage an On-Premises Data Gateway](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-manage)
- [Row-Level Security (RLS) with Power BI](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls)
