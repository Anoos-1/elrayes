"""
UI/UX REDESIGN DOCUMENTATION
Modern Dashboard-Based Financial Management System
===================================================

## 📋 OVERVIEW

The financial system has been redesigned from a crowded single-screen dashboard
into a clean, modular dashboard system with proper UX flow and scalability.

## 🏗️ ARCHITECTURE

### File Structure
```
ui/
├── dashboard.py           # Main dashboard with module cards
├── main_window_new.py     # Navigation hub (new main window)
├── base_layout.py         # Reusable layout components
├── style.py               # Modern style system & color palettes
├── suppliers.py           # Suppliers module page
├── customers.py           # Customers module page
├── bank.py                # Banks module page
├── treasury.py            # Treasury module page
├── master_data.py         # Admin/Master Data module page
└── [other files]
```

## 🎨 DESIGN SYSTEM

### 1. COLOR PALETTES (Modern, Professional)

Each module has a unique color identity:

**Suppliers (الموردين)**
- Primary: #e74c3c (Red/Rose)
- Secondary: #fadab9 (Light rose)
- Dark: #c0392b

**Customers (العملاء)**
- Primary: #3498db (Blue)
- Secondary: #d6eaf8 (Light blue)
- Dark: #2980b9

**Banks (البنوك)**
- Primary: #27ae60 (Green)
- Secondary: #d5f4e6 (Light green)
- Dark: #229954

**Treasury (الخزنة)**
- Primary: #f39c12 (Orange/Gold)
- Secondary: #fce8cc (Light orange)
- Dark: #d68910

**Admin (الإدارة)**
- Primary: #9b59b6 (Purple)
- Secondary: #e8d5f2 (Light purple)
- Dark: #7d3c98

**Neutral Colors**
- White: #ffffff
- Light Gray: #f8f9fa
- Medium Gray: #ecf0f1
- Text Primary: #2c3e50
- Border: #d5dbdb

### 2. TYPOGRAPHY

- **Titles**: Arial, Bold, 24pt (large), 18pt (medium), 14pt (small)
- **Body**: Arial, Regular, 12pt (large), 11pt (medium), 10pt (small)
- **Captions**: Arial, Regular, 9pt
- **Font Family**: Arial (supports Arabic well)

### 3. SPACING & LAYOUT

- **Padding**: 8px, 16px, 24px, 32px
- **Margins**: 30px (page), 20px (sections), 15px (items)
- **Border Radius**: 4px (inputs), 6px (buttons), 8px (cards)
- **Min Heights**: 32px (buttons/inputs), 60px (header), 180px (cards)

## 🔄 USER FLOW

### 1. Application Launch
```
main.py
  ↓
MainWindow (Navigation Hub) created
  ↓
Dashboard page is shown (default)
```

### 2. Dashboard Home Page
- User sees 5 module cards (in grid layout)
- Each card has:
  - Large emoji icon (visual identifier)
  - Arabic title
  - Short description
  - Hover effect (border color + background change)
- Clicking card navigates to module

### 3. Module Page Layout
```
┌─────────────────────────────────┐
│  Navigation Bar (Back button)   │  ← Hidden on dashboard, shown on modules
├─────────────────────────────────┤
│        Module Header            │  ← Color-coded per module
│    (Title + Subtitle)           │
├─────────────────────────────────┤
│     Action Section              │  ← Buttons to add/import/export
│  (إضافة, تسجيل, تحصيل, etc.)    │
├─────────────────────────────────┤
│     Filter Section              │  ← Search/filter before table
│   (Search, Dropdown filters)    │
├─────────────────────────────────┤
│                                 │
│     Data Table                  │  ← Main data display
│  (Suppliers/Customers/etc.)     │
│                                 │
└─────────────────────────────────┘
```

### 4. RTL Support
- All layouts set to `setLayoutDirection(Qt.RightToLeft)`
- Text alignment defaults to right
- Navigation bar back button on left (RTL-aware positioning)

## 🧩 COMPONENT BREAKDOWN

### DashboardCard (ui/dashboard.py)
Modern clickable card for module selection
```python
card = DashboardCard(
    title="الموردين",
    description="إدارة الموردين",
    icon_char="📦",
    color="#e74c3c"
)
card.clicked.connect(on_card_clicked)
```

### ModuleLayout (ui/base_layout.py)
Base template for all module pages
```python
layout = ModuleLayout(title="الموردين", color="#e74c3c")
layout.add_action_section("الإجراءات", [
    ("إضافة مورد", self.add_supplier),
    ("تسجيل عملية", self.record_operation),
])
layout.add_filter_section([
    ("اسم المورد", "text"),
    ("المنطقة", "select"),
])
```

### ActionSection (ui/base_layout.py)
Buttons grouped in a styled card
```python
action_section = ActionSection(
    "الإجراءات",
    [
        ("إضافة مورد", self.add_supplier),
        ("تسجيل عملية", self.record_operation),
    ]
)
```

### FilterSection (ui/base_layout.py)
Search/filter bar for tables
```python
filter_section = FilterSection([
    ("اسم المورد", "text"),
    ("المنطقة", "select"),
    ("الرصيد الأدنى", "number"),
])
```

## 📱 RESPONSIVE DESIGN

- **Dashboard Grid**: 3 columns on large screens
  - Grows: 3 modules per row
  - Cards: Fixed 280×180px
  - Scalable by adding more cards to grid

- **Module Pages**: Full-width
  - Content: Max 1400px
  - Margins: 30px on each side
  - Tables: Scrollable if too wide

## 🎯 UX IMPROVEMENTS

### Before (Old Design)
- ❌ All sections cramped on one page
- ❌ No clear hierarchy
- ❌ Overcrowded buttons and tables
- ❌ Difficult to focus on one task
- ❌ Bad on smaller screens

### After (New Design)
- ✅ Clean dashboard with module selection
- ✅ Dedicated page for each module
- ✅ Clear action sections
- ✅ Organized filters
- ✅ Responsive layout
- ✅ Consistent styling across all modules
- ✅ Easy to add new modules
- ✅ Professional appearance
- ✅ Better visual hierarchy
- ✅ Improved navigation

## 🛠️ HOW TO USE

### 1. Run the Application
```bash
python main.py
```

You'll see:
1. Dashboard home page with 5 module cards
2. Click a card to enter that module
3. Click back button to return to dashboard

### 2. Add a New Module

1. Create new page file: `ui/new_module.py`
   ```python
   from ui.base_layout import ModuleLayout
   
   class NewModulePage(ModuleLayout):
       def __init__(self):
           super().__init__(
               title="الوحدة الجديدة",
               color="#xyz"  # Choose a color
           )
           self.setup_ui()
       
       def setup_ui(self):
           self.add_action_section("الإجراءات", [
               ("إضافة", self.add),
               ("تحرير", self.edit),
           ])
           ...
   ```

2. Register in `main_window_new.py`:
   ```python
   from ui.new_module import NewModulePage
   
   # In _create_pages():
   self.pages['new_module'] = NewModulePage()
   
   # In _on_module_selected():
   module_map['new_module'] = ('new_module', 'الوحدة الجديدة')
   ```

3. Add card to dashboard (`ui/dashboard.py`):
   ```python
   modules = [
       ...
       ("الوحدة الجديدة", "الوصف", "🆕", "#xyz", "new_module"),
   ]
   ```

### 3. Customize Colors

Edit `ui/style.py` COLORS dictionary:
```python
COLORS = {
    'my_module': {
        'primary': '#your_color',
        'secondary': '#light_variant',
        'dark': '#dark_variant',
        'text': '#2c3e50',
    },
    ...
}
```

## 📊 CURRENT MODULES

1. **Suppliers (الموردين)** - Supplier management
   - Add/edit/delete suppliers
   - Record operations
   - View balances

2. **Customers (العملاء)** - Customer management
   - Add/edit/delete customers
   - Record transactions
   - View collections

3. **Banks (البنوك)** - Bank account management
   - Add/edit/delete bank accounts
   - Track balances

4. **Treasury (الخزنة)** - Cash management
   - Record cash transactions
   - Bank transfers
   - Discount tracking

5. **Admin (الإدارة)** - Master data
   - Item types
   - Companies
   - System configuration

## 🚀 FEATURES

✅ Modern Dashboard
✅ Clean Module Pages
✅ Consistent Styling
✅ Arabic RTL Support
✅ Color-Coded Modules
✅ Organized Actions
✅ Filterable Tables
✅ Responsive Layout
✅ Easy Module Addition
✅ Professional Appearance
✅ Hover Effects
✅ Clear Typography
✅ Proper Spacing
✅ Modern Colors
✅ Reusable Components

## 📝 NOTES

- All colors are modern and professional
- Components are fully reusable
- System is designed for scalability
- Easy to add new modules
- RTL layout support built-in
- All files follow PEP 8 style guide
- Comprehensive error handling
- Database integration ready

## 🔮 FUTURE ENHANCEMENTS

Optional improvements:
- Dashboard widgets (quick stats)
- Sidebar navigation (alternative to back button)
- Dark mode toggle
- Theme customization
- Module icons instead of emoji
- Breadcrumb navigation
- Search across all modules
- Recent activities dashboard
- Export/import functionality
- User preferences

"""
