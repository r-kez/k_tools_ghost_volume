# K-Tools: Ghost Volume

A professional-grade Blender extension designed for high-precision physical product prototyping. This tool provides real-time volume measurements in various units (ml, L, m³, fl oz) directly in the 3D viewport.

## 🚀 Key Features

- **Real-time Engine**: Live volume updates while you move, rotate, or edit vertices.
- **Ghost Proxy System**: Specifically designed for open meshes. It automatically "caps" your model in memory to calculate exact internal volume.
- **Liquid Height (Waterline)**: Set a specific height relative to the object's base to simulate liquid fill levels.
- **Vertex Group Targeting**: Assign specific faces (the "Volume Source") to exclude handles or external parts from the measurement.
- **Multiple Units**: Toggle between Milliliters (ml), Liters (L), Cubic Meters (m³), and Fluid Ounces (fl oz).
- **GPU Viewport Overlay**: Professional data display that follows your object in 3D space.

## 🛠 How to Use

### 1. Basic Measurement
1. Select your mesh object.
2. Open the **N-Panel** (Sidebar) and find the **K-Tools** tab.
3. Click **Start Real-time** to begin monitoring the volume.

### 2. Using the Waterline (Liquid Level)
1. Enable **Use Waterline**.
2. Adjust the **Liquid Height** slider. 
3. A blue semi-transparent plane will appear, representing the liquid surface. The volume shown will be the space *below* this plane.

### 3. Measuring Open Containers (e.g., a Cup)
1. Ensure **Precision Mode** (Cog icon) is active.
2. The add-on will automatically find the "rim" of your container and close it in the background to get a perfect volume reading.

### 4. Selection Mode
1. Create a **Vertex Group** containing only the faces that define the volume.
2. In the add-on panel, enable **Use Selection** and search for your Vertex Group.
3. Only the volume contained by those specific faces will be calculated.

## ⚙️ Technical Details

- **Engine**: Pure BMesh-based geometric summation.
- **Performance**: High-poly support via "Fast Mode" mathematical estimation.
- **Architecture**: Modular Python structure for maximum stability and easy expansion.

---
*Developed for professional physical prototyping and industrial design.*
