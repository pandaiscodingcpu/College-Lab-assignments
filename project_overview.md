# Smart Recipe Recommender & Meal Planner
## Project Overview (2-Day Implementation)

---

## 📋 Executive Summary

A desktop application that manages recipes, tracks nutrition, and provides ML-powered recommendations. Built with Python, Tkinter, scikit-learn, and Seaborn. Designed for completion in 2 days with core features prioritized for immediate usability.

**Tech Stack**: Python 3.7+ | Tkinter | SQLite | scikit-learn | Seaborn | Matplotlib

---

## 🎯 Core Features (Priority Order)

### Day 1: Foundation (6-8 hours)
1. **Database Setup** - SQLite schema and CRUD operations
2. **Recipe Management** - Add, view, search, delete recipes
3. **Basic GUI** - Main window with recipe browser
4. **CSV Import** - Bulk import sample recipes

### Day 2: ML & Visualization (6-8 hours)
5. **ML Models** - Recipe recommender and time predictor
6. **Meal Logging** - Track consumed meals
7. **Visualizations** - Nutrition and recipe analytics
8. **File Export** - Reports and shopping lists

---

## 🗄️ Database Schema

### **1. recipes**
Stores core recipe information and nutrition data.

```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cuisine TEXT,
    cooking_time INTEGER,           -- in minutes
    difficulty TEXT,                -- Easy, Medium, Hard
    instructions TEXT,
    calories INTEGER,
    protein REAL,                   -- in grams
    carbs REAL,                     -- in grams
    fats REAL,                      -- in grams
    date_added TEXT                 -- YYYY-MM-DD
);
```

**Sample Data:**
| id | name | cuisine | cooking_time | difficulty | calories |
|----|------|---------|--------------|------------|----------|
| 1 | Spaghetti Carbonara | Italian | 25 | Medium | 450 |
| 2 | Chicken Curry | Indian | 40 | Medium | 380 |
| 3 | Caesar Salad | American | 15 | Easy | 320 |

---

### **2. ingredients**
Master list of all ingredients used across recipes.

```sql
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT,                  -- Vegetable, Protein, Dairy, etc.
    unit TEXT                       -- g, ml, cups, etc.
);
```

**Sample Data:**
| id | name | category | unit |
|----|------|----------|------|
| 1 | pasta | Grain | g |
| 2 | chicken | Protein | g |
| 3 | tomato | Vegetable | pieces |

---

### **3. recipe_ingredients**
Junction table linking recipes to ingredients (Many-to-Many).

```sql
CREATE TABLE recipe_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER,
    ingredient_id INTEGER,
    quantity TEXT,                  -- "200g", "2 cups", "3 pieces"
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);
```

**Sample Data:**
| id | recipe_id | ingredient_id | quantity |
|----|-----------|---------------|----------|
| 1 | 1 | 1 | 200g |
| 2 | 1 | 4 | 100g |
| 3 | 2 | 2 | 300g |

---

### **4. meal_history**
Tracks meals consumed by user with ratings and notes.

```sql
CREATE TABLE meal_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER,
    date_consumed TEXT,             -- YYYY-MM-DD
    rating INTEGER,                 -- 1-5 stars
    notes TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
```

**Sample Data:**
| id | recipe_id | date_consumed | rating | notes |
|----|-----------|---------------|--------|-------|
| 1 | 1 | 2025-11-01 | 5 | Perfect! |
| 2 | 2 | 2025-11-02 | 4 | Too spicy |
| 3 | 1 | 2025-11-03 | 5 | Family favorite |

---

### **5. nutrition_log**
Aggregated daily nutrition data for tracking and visualization.

```sql
CREATE TABLE nutrition_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,                      -- YYYY-MM-DD
    calories REAL,
    protein REAL,
    carbs REAL,
    fats REAL,
    recipe_id INTEGER,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
```

**Sample Data:**
| id | date | calories | protein | carbs | fats |
|----|------|----------|---------|-------|------|
| 1 | 2025-11-01 | 450 | 18 | 52 | 16 |
| 2 | 2025-11-02 | 380 | 32 | 28 | 14 |
| 3 | 2025-11-03 | 450 | 18 | 52 | 16 |

---

### **6. user_pantry** (Optional - Time Permitting)
Tracks available ingredients in user's pantry.

```sql
CREATE TABLE user_pantry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER,
    quantity_available TEXT,
    last_updated TEXT,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);
```

---

## 🤖 Machine Learning Models

### **Model 1: Recipe Recommender (K-Means Clustering)**

**Purpose**: Group similar recipes and recommend alternatives based on user preferences.

**Algorithm**: K-Means Clustering (Unsupervised Learning)

**Feature Engineering**:
```python
Features = [
    ingredient_count,           # Number of ingredients
    cuisine_encoded,            # Label encoded cuisine type
    difficulty_encoded,         # Easy=0, Medium=1, Hard=2
    cooking_time_normalized,    # Scaled 0-1
    calories_normalized         # Scaled 0-1
]
```

**Training Process**:
1. Extract features from all recipes in database
2. Normalize numerical features using StandardScaler
3. Apply K-Means with k=5 clusters (or n_recipes/3, whichever is smaller)
4. Store cluster assignments with recipe IDs

**Prediction/Recommendation**:
```python
def recommend_similar_recipes(recipe_id, n=5):
    # Find cluster of selected recipe
    cluster = get_recipe_cluster(recipe_id)
    
    # Get all recipes in same cluster
    similar_recipes = get_recipes_by_cluster(cluster)
    
    # Exclude the selected recipe
    similar_recipes = [r for r in similar_recipes if r.id != recipe_id]
    
    # Return top n similar recipes
    return similar_recipes[:n]
```

**Example Output**:
```
User selects: "Spaghetti Carbonara" (Cluster 2)

Recommendations from Cluster 2:
1. Pasta Alfredo (Italian, Medium, 30 min)
2. Penne Arrabiata (Italian, Easy, 20 min)
3. Lasagna (Italian, Hard, 60 min)
4. Cacio e Pepe (Italian, Easy, 15 min)
5. Pesto Pasta (Italian, Easy, 20 min)
```

---

### **Model 2: Cooking Time Predictor (Linear Regression)**

**Purpose**: Predict cooking time for new recipes based on complexity.

**Algorithm**: Linear Regression

**Features**:
```python
X = [
    ingredient_count,
    cuisine_encoded,
    difficulty_encoded,
    calories
]

y = cooking_time  # Target variable in minutes
```

**Training**:
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Prediction accuracy: ±{mae:.1f} minutes")
```

**Use Case**: When user adds a new recipe, predict cooking time automatically.

**Example**:
```
Input:
- Ingredients: 8 items
- Cuisine: Thai
- Difficulty: Hard
- Calories: 420

Predicted Time: 35 minutes (±10 min)
```

---

### **Model 3: Recipe Category Classifier (Random Forest)** *(Optional)*

**Purpose**: Auto-classify recipes as Breakfast/Lunch/Dinner/Snack.

**Algorithm**: Random Forest Classifier

**Features**: `[ingredient_count, cooking_time, calories, protein]`

**Simple Heuristic** (if time-constrained):
```python
if calories < 300 and cooking_time < 20:
    return "Snack"
elif cooking_time < 25:
    return "Breakfast"
elif calories > 400:
    return "Dinner"
else:
    return "Lunch"
```

---

## 📊 Data Visualizations

### **Dashboard 1: Nutrition Tracker**

**Purpose**: Monitor daily calorie intake and macronutrient balance.

**Charts**:

#### **1.1 Daily Calorie Trend (Line Chart)**
```python
# Seaborn line plot
sns.lineplot(data=nutrition_df, x='date', y='calories', marker='o')
plt.title('Daily Calorie Intake')
plt.ylabel('Calories')
plt.xticks(rotation=45)
```

**Data Source**: `nutrition_log` table, last 30 days

**Sample Visualization**:
```
Calories
  500 |     ●
  450 |   ●   ●     ●
  400 | ●       ●       ●
  350 |                   ●
  300 +---+---+---+---+---+---+---
      1   2   3   4   5   6   7  (Days)
```

**Insights**:
- Average daily intake: 412 calories
- Trend: Slightly increasing
- Goal comparison: Under target (2000 cal/day)

---

#### **1.2 Macronutrient Breakdown (Stacked Bar Chart)**
```python
# Create stacked bar chart
data = nutrition_df.groupby('date')[['protein', 'carbs', 'fats']].sum()
data.plot(kind='bar', stacked=True, color=['#FF6B6B', '#4ECDC4', '#FFE66D'])
plt.title('Daily Macronutrient Breakdown')
plt.ylabel('Grams')
```

**Sample Visualization**:
```
Grams
 100 |     [Fats]
  80 |     [Carbs]
  60 |     [Protein]
  40 |
  20 |
   0 +---+---+---+---+---+
      M   T   W   T   F
```

**Insights**:
- Carbs: 55% (average 52g/day)
- Protein: 25% (average 24g/day)
- Fats: 20% (average 16g/day)

---

#### **1.3 Weekly Macronutrient Pie Chart**
```python
# Aggregate last 7 days
totals = {
    'Protein': sum(protein_values),
    'Carbs': sum(carbs_values),
    'Fats': sum(fats_values)
}

plt.pie(totals.values(), labels=totals.keys(), autopct='%1.1f%%')
plt.title('Weekly Macronutrient Distribution')
```

**Sample Output**:
- Protein: 25.5% (140g total)
- Carbs: 54.8% (302g total)
- Fats: 19.7% (108g total)

---

### **Dashboard 2: Recipe Analytics**

#### **2.1 Most Cooked Recipes (Horizontal Bar Chart)**
```python
# Query top 10 recipes from meal_history
top_recipes = """
    SELECT r.name, COUNT(*) as count
    FROM meal_history mh
    JOIN recipes r ON mh.recipe_id = r.id
    GROUP BY r.id
    ORDER BY count DESC
    LIMIT 10
"""

sns.barplot(data=df, x='count', y='name', palette='viridis')
plt.title('Top 10 Most Cooked Recipes')
```

**Sample Data**:
```
Spaghetti Carbonara    ████████████ 12
Chicken Curry          ██████████ 10
Vegetable Stir Fry     ████████ 8
Pancakes               ███████ 7
Caesar Salad           ██████ 6
```

**Insights**:
- Italian cuisine dominates (40%)
- Quick recipes (<30 min) cooked more frequently
- Pasta dishes are most popular

---

#### **2.2 Cuisine Distribution (Pie Chart)**
```python
cuisine_counts = recipes_df['cuisine'].value_counts()
plt.pie(cuisine_counts, labels=cuisine_counts.index, autopct='%1.1f%%')
plt.title('Recipe Collection by Cuisine')
```

**Sample Output**:
- Italian: 25% (8 recipes)
- Indian: 20% (6 recipes)
- American: 18% (5 recipes)
- Chinese: 15% (4 recipes)
- Thai: 12% (3 recipes)
- Others: 10% (4 recipes)

---

#### **2.3 Cooking Time by Difficulty (Box Plot)**
```python
sns.boxplot(data=recipes_df, x='difficulty', y='cooking_time', palette='Set2')
plt.title('Cooking Time Distribution by Difficulty')
plt.ylabel('Minutes')
```

**Sample Insights**:
```
Minutes
  90 |              x (outlier)
  75 |            [---]
  60 |            |   |
  45 |      [---] |   |
  30 |[---] |   | |   |
  15 ||   | |   | |   |
   0 +-----+-----+-----+
     Easy  Med   Hard
```

- Easy: 10-25 min (median: 15 min)
- Medium: 20-45 min (median: 30 min)
- Hard: 35-90 min (median: 50 min)

---

#### **2.4 Ingredients per Recipe (Histogram)**
```python
plt.hist(ingredient_counts, bins=10, color='#4ECDC4', edgecolor='black')
plt.title('Distribution of Ingredient Count per Recipe')
plt.xlabel('Number of Ingredients')
plt.ylabel('Frequency')
```

**Sample Distribution**:
```
Frequency
  10 |     █
   8 |     █ █
   6 | █   █ █ █
   4 | █ █ █ █ █
   2 | █ █ █ █ █ █
   0 +---+---+---+---+---+
      2   4   6   8  10  12
      (Number of Ingredients)
```

**Insights**:
- Most recipes: 5-8 ingredients
- Simple recipes (<5 ingredients): 15%
- Complex recipes (>10 ingredients): 10%

---

### **Dashboard 3: Ingredient Analytics**

#### **3.1 Top Ingredients Across All Recipes (Bar Chart)**
```python
# Count ingredient occurrences
ingredient_freq = """
    SELECT i.name, COUNT(*) as frequency
    FROM recipe_ingredients ri
    JOIN ingredients i ON ri.ingredient_id = i.id
    GROUP BY i.id
    ORDER BY frequency DESC
    LIMIT 15
"""

plt.barh(ingredients, frequencies, color='#FFE66D')
plt.title('Most Used Ingredients (Top 15)')
```

**Sample Data**:
```
Onion              ████████████████ 18
Garlic             ███████████████ 15
Tomato             ████████████ 12
Chicken            ██████████ 10
Olive Oil          █████████ 9
Salt               █████████ 9
```

**Insights**:
- Onion is in 60% of all recipes
- Garlic in 50% of recipes
- Most versatile ingredients: onion, garlic, tomato

---

#### **3.2 Ingredient Category Distribution (Donut Chart)**
```python
category_counts = ingredients_df['category'].value_counts()
colors = sns.color_palette('pastel')

plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
        colors=colors, wedgeprops={'width': 0.4})
plt.title('Ingredients by Category')
```

**Sample Output**:
- Vegetables: 35%
- Proteins: 25%
- Grains: 15%
- Dairy: 12%
- Spices: 8%
- Others: 5%

---

#### **3.3 Ingredient-Recipe Heatmap**
```python
# Create presence matrix (recipes × top 20 ingredients)
presence_matrix = create_ingredient_presence_matrix()

sns.heatmap(presence_matrix, cmap='YlOrRd', cbar_kws={'label': 'Present'})
plt.title('Ingredient Usage Across Recipes')
plt.xlabel('Ingredients')
plt.ylabel('Recipes')
```

**Sample Heatmap**:
```
                Onion Garlic Tomato Chicken Rice
Spaghetti       ■     ■      □      □       □
Chicken Curry   ■     ■      ■      ■       ■
Caesar Salad    ■     □      ■      ■       □
Fried Rice      ■     ■      □      □       ■
```
■ = Present, □ = Absent

**Insights**:
- Ingredient clusters: Italian recipes share similar ingredients
- Recipe similarity visible through ingredient patterns

---

### **Dashboard 4: ML Insights**

#### **4.1 Recipe Similarity Network (Scatter Plot with Clusters)**
```python
# Apply PCA to reduce clustering features to 2D
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
coords = pca.fit_transform(scaled_features)

plt.scatter(coords[:, 0], coords[:, 1], c=cluster_labels, cmap='viridis', s=100)
plt.title('Recipe Similarity Map (ML Clustering)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')

# Add recipe names as labels
for i, name in enumerate(recipe_names):
    plt.annotate(name, (coords[i, 0], coords[i, 1]), fontsize=8)
```

**Sample Visualization**:
```
PC2
  | Cluster 2 (Thai)
  |    ● Pad Thai
  |    ● Tom Yum
  |
  | Cluster 1 (Italian)
  | ● Carbonara  ● Pizza
  | ● Lasagna
  |
  +---● Curry (Indian)----------- PC1
      ● Biryani
      Cluster 3 (Indian)
```

**Insights**:
- 5 distinct recipe clusters identified
- Cuisines naturally group together
- Cross-cuisine similarities (e.g., Rice dishes)

---

#### **4.2 Prediction Accuracy (Scatter Plot)**
```python
# Cooking time: Predicted vs Actual
plt.scatter(actual_times, predicted_times, alpha=0.6)
plt.plot([0, 90], [0, 90], 'r--', label='Perfect Prediction')
plt.title('Cooking Time Prediction Accuracy')
plt.xlabel('Actual Time (min)')
plt.ylabel('Predicted Time (min)')
plt.legend()
```

**Sample Output**:
- MAE (Mean Absolute Error): ±8.5 minutes
- R² Score: 0.82 (good fit)
- Prediction range: 10-90 minutes

---

## 🖥️ GUI Menu Structure

### **Main Window Layout**

```
┌─────────────────────────────────────────────────────┐
│  🍽️ Smart Recipe Planner          [Import] [Train] │
├─────────────────────────────────────────────────────┤
│ [Dashboard] [Recipes] [Add] [Meal Log] [Analytics] │
├─────────────────────────────────────────────────────┤
│                                                     │
│                  Content Area                       │
│              (Tab-specific content)                 │
│                                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### **Tab 1: Dashboard** (Home Screen)

```
┌─────────────────────────────────────────────────────┐
│ 📊 Dashboard                                         │
├─────────────────────────────────────────────────────┤
│ Today: Monday, November 03, 2025                    │
│                                                     │
│ Quick Stats                                         │
│ ├─ Total Recipes: 30                               │
│ ├─ Meals Logged (30 days): 45                      │
│ └─ Pantry Items: 12                                │
│                                                     │
│ Recent Meals (Last 7 Days)                          │
│ ┌─────────────────────────────────────────────┐    │
│ │ Date       │ Recipe           │ Rating       │    │
│ ├────────────┼──────────────────┼──────────────┤    │
│ │ 2025-11-01 │ Spaghetti        │ ⭐⭐⭐⭐⭐    │    │
│ │ 2025-11-02 │ Chicken Curry    │ ⭐⭐⭐⭐      │    │
│ │ 2025-11-02 │ Caesar Salad     │ ⭐⭐⭐⭐⭐    │    │
│ │ ...        │ ...              │ ...          │    │
│ └─────────────────────────────────────────────┘    │
│                                       [View More]   │
└─────────────────────────────────────────────────────┘
```

---

### **Tab 2: Recipes** (Browse & Search)

```
┌─────────────────────────────────────────────────────┐
│ 📖 Recipes                                           │
├─────────────────────────────────────────────────────┤
│ Search: [_______________] [Search] [Show All]       │
│                                                     │
│ Recipe List (Page 1 of 3)          Showing 1-10/30 │
│ ┌─────────────────────────────────────────────┐    │
│ │ID│Name          │Cuisine│Time │Diff │Calories│   │
│ ├──┼──────────────┼───────┼─────┼─────┼────────┤   │
│ │1 │Spaghetti     │Italian│25m  │Med  │450     │   │
│ │2 │Chicken Curry │Indian │40m  │Med  │380     │   │
│ │3 │Caesar Salad  │Amer   │15m  │Easy │320     │   │
│ │4 │Pad Thai      │Thai   │35m  │Hard │420     │   │
│ │5 │Greek Salad   │Greek  │10m  │Easy │180     │   │
│ │6 │Beef Tacos    │Mexican│20m  │Easy │380     │   │
│ │7 │Mushroom Riso │Italian│45m  │Hard │340     │   │
│ │8 │Salmon Teri   │Japan  │25m  │Med  │420     │   │
│ │9 │Veg Stir Fry  │Chinese│15m  │Easy │220     │   │
│ │10│Pancakes      │Amer   │20m  │Easy │280     │   │
│ └─────────────────────────────────────────────┘    │
│                                                     │
│ [View Details] [Shopping List] [Delete]             │
│ [< Previous]  Page 1 of 3  [Next >]                │
└─────────────────────────────────────────────────────┘
```

**Pagination Logic**:
- 10 recipes per page
- Total pages = ceil(total_recipes / 10)
- Navigation buttons disabled at boundaries

---

### **Tab 3: Add Recipe**

```
┌─────────────────────────────────────────────────────┐
│ ➕ Add Recipe                     [Scrollable Form] │
├─────────────────────────────────────────────────────┤
│ Recipe Information                                  │
│ ├─ Recipe Name:* [_________________________]       │
│ ├─ Cuisine:      [Italian ▼]                       │
│ ├─ Difficulty:   [Medium ▼]                        │
│ └─ Cooking Time: [___] min  [Predict Time (ML)]    │
│                                                     │
│ Nutrition Per Serving                               │
│ ├─ Calories: [___]  Protein: [___]g                │
│ └─ Carbs:    [___]g Fats:    [___]g                │
│                                                     │
│ Ingredients                                         │
│ ├─ Ingredient: [________] Qty: [____] [Add]        │
│ └─ List:                                            │
│    ┌────────────────────────┐                      │
│    │ pasta: 200g           │ [Remove]              │
│    │ bacon: 100g           │ [Remove]              │
│    │ eggs: 2               │ [Remove]              │
│    └────────────────────────┘                      │
│                                                     │
│ Cooking Instructions                                │
│ ┌───────────────────────────────────────────┐      │
│ │ 1. Boil pasta in salted water...         │      │
│ │ 2. Fry bacon until crispy...             │      │
│ │ ...                                       │      │
│ └───────────────────────────────────────────┘      │
│                                                     │
│ [Save Recipe] [Clear Form]                          │
└─────────────────────────────────────────────────────┘
```

---

### **Tab 4: Meal Log**

```
┌─────────────────────────────────────────────────────┐
│ 📝 Log Meal                                          │
├─────────────────────────────────────────────────────┤
│ Log a Meal                                          │
│ ├─ Recipe:  [Spaghetti Carbonara ▼]                │
│ ├─ Date:    [2025-11-03_______________]            │
│ ├─ Rating:  [⭐⭐⭐⭐⭐] (5 stars)                    │
│ └─ Notes:                                           │
│    ┌────────────────────────────────────┐          │
│    │ Perfect! Family loved it.         │          │
│    └────────────────────────────────────┘          │
│                                                     │
│ [Log Meal]                                          │
│                                                     │
│ ─────────────────────────────────────────          │
│                                                     │
│ Export                                              │
│ [Export Nutrition Report] [Export Meal Plan]        │
└─────────────────────────────────────────────────────┘
```

---

### **Tab 5: Analytics** (Visualizations)

```
┌─────────────────────────────────────────────────────┐
│ 📈 Analytics                                         │
├─────────────────────────────────────────────────────┤
│ Select Chart: [Nutrition Trends ▼] [Generate]      │
│                                                     │
│ ┌─────────────────────────────────────────────┐    │
│ │      Daily Calorie Intake (Last 30 Days)   │    │
│ │ 500 ┤        ●                               │    │
│ │ 450 ┤    ●       ●   ●                       │    │
│ │ 400 ┤  ●                   ●                 │    │
│ │ 350 ┤                                        │    │
│ │ 300 └─────────────────────────────────────  │    │
│ │       Oct 05  Oct 12  Oct 19  Oct 26       │    │
│ │                                              │    │
│ │    Macronutrient Breakdown                  │    │
│ │  80 ┤ █ █ █ █ █  [Fats]                     │    │
│ │  60 ┤ █ █ █ █ █  [Carbs]                    │    │
│ │  40 ┤ █ █ █ █ █  [Protein]                  │    │
│ │  20 ┤ █ █ █ █ █                             │    │
│ │   0 └──────────────                         │    │
│ │      M  T  W  T  F                          │    │
│ └─────────────────────────────────────────────┘    │
│                                                     │
│ Chart Options:                                      │
│ • Nutrition Trends                                  │
│ • Macronutrient Pie                                 │
│ • Most Cooked Recipes                               │
│ • Cuisine Distribution                              │
│ • Cooking Time by Difficulty                        │
│ • Calories vs Time                                  │
└─────────────────────────────────────────────────────┘
```

---

### **Tab 6: ML Insights**

```
┌─────────────────────────────────────────────────────┐
│ 🤖 ML Insights                                       │
├─────────────────────────────────────────────────────┤
│ Recipe Recommendations                              │
│                                                     │
│ Select a recipe to get recommendations:             │
│ [Spaghetti Carbonara_____▼]                        │
│                                                     │
│ [Get Recommendations]                               │
│                                                     │
│ ┌─────────────────────────────────────────────┐    │
│ │ Recipes similar to 'Spaghetti Carbonara':  │    │
│ │                                              │    │
│ │ These recipes are in the same cluster      │    │
│ │ based on ingredients, cooking time, and     │    │
│ │ difficulty:                                  │    │
│ │                                              │    │
│ │ 1. Pasta Alfredo                            │    │
│ │    ├─ Cuisine: Italian                      │    │
│ │    ├─ Time: 30 minutes                      │    │
│ │    └─ Difficulty: Medium                    │    │
│ │                                              │    │
│ │ 2. Cacio e Pepe                             │    │
│