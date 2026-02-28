import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ==============================
# 1. Load Dataset
# ==============================

data = pd.read_csv("dataset_complete.csv")

print("Dataset Loaded Successfully")
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])

# ==============================
# 2. Create Total Power Column
# ==============================

data["total_power"] = (
    data["active_power_1"] +
    data["active_power_2"] +
    data["active_power_3"] +
    data["active_power_4"] +
    data["active_power_5"] +
    data["active_power_6"]
)

# ==============================
# 3. Drop Unnecessary Columns
# ==============================

data = data.drop(columns=["timestamp", "source"])

# Remove rows with missing values
data = data.dropna()

print("Data cleaned successfully")

# ==============================
# 4. Define Features (X) and Target (y)
# ==============================

X = data.drop(columns=[
    "active_power_1",
    "active_power_2",
    "active_power_3",
    "active_power_4",
    "active_power_5",
    "active_power_6",
    "total_power"
])

y = data["total_power"]

print("Feature selection done")
print("Number of features:", X.shape[1])

# ==============================
# 5. Train-Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train-Test split completed")

# ==============================
# 6. Train Model
# ==============================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
print("Model training completed")

# ==============================
# 7. Make Predictions
# ==============================

predictions = model.predict(X_test)

# ==============================
# 8. Evaluate Model
# ==============================

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n===== MODEL PERFORMANCE =====")
print("MAE:", round(mae, 3))
print("R2 Score:", round(r2, 3))
print("=============================")
import joblib
joblib.dump(model, "power_model.pkl")
print("Model saved successfully as power_model.pkl")