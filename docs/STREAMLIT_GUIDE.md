# Streamlit Compliance Checker - User Guide

## 🚀 Quick Start

### Starting the App

```bash
# Option 1: Use the launcher script
./run_app.sh

# Option 2: Manual start
source venv/bin/activate
streamlit run app.py
```

The app will open automatically at: **http://localhost:8501**

---

## 📋 Step-by-Step Usage

### 1️⃣ **First Time Setup - Build Knowledge Base**

Before analyzing any documents, you need to build the regulatory knowledge base:

1. Look at the **left sidebar**
2. Scroll down to find **"🔨 Build Knowledge Base"** button
3. Click it and wait ~2-3 minutes
4. You'll see "✅ Knowledge base ready" when complete

**This only needs to be done once!** The knowledge base is cached.

---

### 2️⃣ **Quick Demo - Load Pre-Generated Results**

To instantly see the UI without waiting for analysis:

1. Click the **"⚡ Load Demo Results"** button
2. Results will appear immediately
3. Explore the visualizations and detailed findings

---

### 3️⃣ **Analyze a Prospectus**

#### Option A: Use Test Files
1. Click one of the test prospectus buttons:
   - 📊 E Fund ETF
   - 📊 ChinaAMC Global
   - 📊 BlackRock Premier

2. Click **"🔍 Analyze Compliance"** button

3. Wait for analysis to complete (this takes several minutes as the LLM processes the document)

4. Results will appear below

#### Option B: Upload Your Own PDF
1. Click **"Browse files"** in the upload section
2. Select a prospectus PDF
3. Click **"🔍 Analyze Compliance"**
4. Wait for analysis
5. View results

---

## 🎨 Understanding the Results

### Summary Metrics (Top Row)
- **Total Violations**: Overall count of issues found
- **Critical**: High-priority compliance violations
- **Warnings**: Lower-priority issues requiring attention
- **Analyzed**: Name of the document checked

### Visualizations
- **Bar Chart**: Shows violations by category (Fee, Risk, Concentration)
- **Pie Chart**: Shows severity distribution (Critical vs Warning)

### Detailed Findings
- Each violation is shown in an expandable card
- Click to view:
  - Severity level
  - Page number
  - Specific issue description
  - Regulatory citation
  - Detailed explanation
  - Prospectus context
  - Relevant regulatory text

---

## ⚠️ Troubleshooting

### "No Report Appears After Clicking Analyze"

**Problem**: Analysis button clicked but no results show

**Solutions**:

1. **Check if Ollama is running**:
   ```bash
   ollama list
   ```
   If you see an error, start Ollama:
   ```bash
   ollama serve
   ```

2. **Check browser console for errors**:
   - Press F12 in your browser
   - Look for any error messages

3. **Try the Demo Results first**:
   - Click "⚡ Load Demo Results" to verify the UI works
   - This eliminates LLM issues

4. **Restart the Streamlit app**:
   - Press `Ctrl+C` in the terminal
   - Run `./run_app.sh` again

5. **Check terminal output**:
   - Look at the terminal where Streamlit is running
   - Check for any error messages

### "Knowledge Base Won't Build"

**Solutions**:
- Verify PDFs are in the correct location:
  ```bash
  ls -la "fund manager code of conduct.pdf"
  ls -la "Code_on_MPF_Investment_Funds.pdf"
  ```
- Check sidebar for green checkmarks next to PDF names

### "Analysis Takes Too Long"

**This is normal!** LLM analysis is slow:
- E Fund ETF: ~10-15 minutes (754 pages)
- Smaller docs: ~5-8 minutes

**Recommendation**: Use "⚡ Load Demo Results" for quick demos

### "App Won't Start"

**Solutions**:
1. Check Python environment:
   ```bash
   source venv/bin/activate
   python --version  # Should be 3.11
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Check port availability:
   ```bash
   lsof -i :8501
   ```
   Kill existing process if needed

---

## 🎯 Tips for Best Experience

### For Demos/Presentations
1. **Use "⚡ Load Demo Results"** for instant results
2. Pre-build knowledge base before the demo
3. Keep Ollama running in the background

### For Actual Analysis
1. **Start with smaller documents** first
2. Monitor terminal output for progress
3. Be patient - LLM analysis is thorough but slow
4. Analysis runs in the background - you can leave it

### UI Tips
1. **Expand violations** to see full details
2. **Download report** for offline viewing
3. **Use the charts** to quickly understand violation patterns
4. **Raw report view** shows the complete text report

---

## 🔧 Advanced Options

### Change LLM Model
- Use the dropdown in the sidebar
- Available models:
  - llama3.1:8b (recommended, faster)
  - llama2:latest
  - llama3.2

### Cache Management
- Knowledge base is cached in `knowledge_base_cache.json`
- Delete this file to rebuild from scratch
- Cached results load instantly

---

## 📊 What Gets Analyzed

The system checks for 3 main compliance areas:

### 1. Fee Disclosure Completeness
- Management fees clearly stated
- Performance fees with calculation methods
- All expenses itemized
- Examples provided

### 2. Risk Disclosure Requirements
- Market risk factors
- Liquidity risk explained
- Currency risk for foreign investments
- Investment-specific risks

### 3. Investment Concentration Limits
- Single issuer exposure limits
- Sector concentration disclosed
- Geographic diversification
- Compliance statements

---

## 💾 Exporting Results

### Download Report
1. Scroll to bottom of results
2. Click **"📥 Download Full Report"**
3. Saves as timestamped text file

### View Raw Report
1. Click **"📄 View Raw Report"** expander
2. Copy text for use in other documents

---

## 🎨 UI Features

### Black Theme Design
- **Professional dark aesthetic** - Black background with subtle grays
- **High contrast** - White text for readability
- **Color-coded severity**:
  - 🔴 Red = Critical violations
  - 🟡 Orange = Warnings
  - ✅ Green = Success messages

### Interactive Elements
- **Hover effects** on buttons
- **Expandable cards** for violations
- **Interactive charts** with Plotly
- **Progress indicators** during analysis

---

## 🚨 Common Error Messages

### "Ollama not accessible"
→ Start Ollama: `ollama serve`

### "PDF not found"
→ Check file is in the same directory as app.py

### "Model not found"
→ Pull the model: `ollama pull llama3.1:8b`

### "Knowledge base not built"
→ Click "Build Knowledge Base" in sidebar first

---

## 📱 Browser Compatibility

**Recommended**:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Note**: Some older browsers may not display charts correctly

---

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Look at terminal output** for error messages
3. **Try demo mode first** to isolate the issue
4. **Restart everything**:
   ```bash
   # Stop Streamlit (Ctrl+C)
   # Restart Ollama
   ollama serve
   
   # Restart app
   ./run_app.sh
   ```

---

## 📈 Performance Notes

- **First analysis is slowest** (building caches)
- **Subsequent analyses** are faster (cached knowledge base)
- **Demo results** load instantly (pre-generated)
- **Large PDFs** (500+ pages) take 15-20 minutes

---

**Built for Klares.io as a Demo Application**  
**Powered by RAG + LLM + Streamlit**
