# ReturnTrack – Reusable Material Impact Dashboard

**ReturnTrack** is a sustainability initiative dashboard built for **Volvo Eicher Commercial Vehicles Ltd. (VECV)**.  
It tracks reusable packaging returns like **PP Boxes, Plastic Bins, Iron Trolleys, and Wooden Pallets**, and calculates:

- ♻️ CO₂ emissions avoided
- 📦 Material saved
- 💰 Cost savings
- 🚛 Truckloads avoided

---

## 🚀 Features

- Add & edit monthly return data with automatic merging
- Reuse-adjusted impact calculations based on item type
- Live reuse tuning via sidebar sliders
- Monthly KPI dashboard (CO₂, cost, material saved)
- CSV download for impact report
- Persistent data storage across sessions

---

## 📦 Tracked Items and Assumptions

| Item Type      | Avg Weight (kg) | Reuse/Month | Unit Cost (₹) |
|----------------|------------------|-------------|----------------|
| PP Box         | 1.2              | 5           | ₹120           |
| Plastic Bin    | 3.0              | 20          | ₹350           |
| Iron Trolley   | 50.0             | 40          | ₹4500          |
| Wooden Pallet  | 18.0             | 15          | ₹450           |

---

## 🧮 Calculation Logic

**Adjusted Units** = Quantity Returned / Reuse Frequency

Then:

- **CO₂ Avoided (kg)** = Adjusted Units × CO₂ factor per item
- **Material Saved (kg)** = Adjusted Units × Item weight
- **Cost Avoided (₹)** = Adjusted Units × Unit cost
- **Truckloads Avoided** = Material Saved / 1200 kg

---

## 🧠 How to Use

### 1. Clone or Download the Project

```bash
git clone https://github.com/your-org/ReturnTrack.git
cd ReturnTrack
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 📁 Files Included

- `app.py` – Streamlit app interface
- `returntrack_logic.py` – Backend calculations
- `requirements.txt` – Python dependencies
- `README.md` – Project overview and usage

---

## 📞 Contact

For inquiries or implementation assistance, contact the developer or sustainability team at VECV.

---