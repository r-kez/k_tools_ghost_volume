# K-Tools: Calculate Volume (ml) - Roadmap

## Phase 1: Core Calculation Engine ✅
- [x] Implement BMesh volume calculation logic.
- [x] Convert Blender Units (BU³) to Milliliters (ml).
- [x] Create a manual calculation operator.

## Phase 2: Performance & Feedback ✅
- [x] Implement real-time calculation using `bpy.app.timers`.
- [x] Optimized Edit Mode support (BMesh copy for live dragging).
- [x] GPU Viewport Overlay (Name and ML display).

## Phase 3: Advanced Geometry Support ✅
- [x] Vertex Group assignment for partial volume calculation.
- [x] "Ghost Proxy" Precision Mode (Capping open meshes via BMesh ops).
- [x] Fast Mode for high-poly estimated calculations.

## Phase 4: Waterline & UI Refinement ✅
- [x] Relative Liquid Height (Waterline Z relative to object base).
- [x] 3D GPU Preview Plane for Liquid Surface.
- [x] Unit Selection (ml, L, m³, fl oz).
- [x] Precision Toggle and Delay settings.

## Phase 5: Production & Architecture ✅
- [x] Full Modular Refactor (logic, ui, ops, props, drawing).
- [x] Implementation of Namespaced PropertyGroup.
- [x] Addon Preferences with documentation links.
- [x] Final code cleanup and Documentation.

**STATUS: 100% COMPLETE - PRODUCTION READY**
