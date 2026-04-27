from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report, f1_score, accuracy_score
import numpy as np

class BoostingEnsemble:
    """
    Boosting technique combining multiple algorithms (Section 4.2)
    """
    def __init__(self):
        self.models = {
            'DT': DecisionTreeClassifier(),
            'RF': RandomForestClassifier(n_estimators=100),
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'NB': BernoulliNB()
        }
        self.weights = {
            'CNN': 0.4,  # Higher weight for CNN
            'DT': 0.15,
            'RF': 0.15,
            'KNN': 0.15,
            'NB': 0.15
        }
    
    def train_all(self, X_train, y_train):
        """Train all boosting models"""
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
    
    def predict_with_boosting(self, X_test, cnn_predictions):
        """
        Combine predictions using weighted F1 scores
        """
        all_predictions = {'CNN': cnn_predictions}
        
        # Get predictions from all models
        for name, model in self.models.items():
            all_predictions[name] = model.predict(X_test)
        
        # Weighted voting
        final_predictions = []
        for i in range(len(X_test)):
            votes = {}
            for model_name, preds in all_predictions.items():
                pred = preds[i]
                votes[pred] = votes.get(pred, 0) + self.weights[model_name]
            
            final_predictions.append(max(votes, key=votes.get))
        
        return np.array(final_predictions)
    
    def evaluate(self, X_test, y_test):
        """Evaluate all models with accuracy and F1-score"""
        results = {}
        print("\n" + "="*60)
        print("BOOSTING MODELS EVALUATION")
        print("="*60)
        for name, model in self.models.items():
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            results[name] = {'accuracy': accuracy, 'f1_score': f1}
            print(f"{name:15} - Accuracy: {accuracy:.4f} | F1-Score: {f1:.4f}")
        print("="*60)
        
        return results