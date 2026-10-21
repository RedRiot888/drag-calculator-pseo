// calculator-core.js - Simple Math Formulas for Drag Racing
const DragCalc = {
    // Quarter-mile ET formula based on weight and horsepower
    quarterMileET(weight, hp) {
        if (!weight || !hp || hp <= 0) return 0;
        return (5.825 * Math.pow(weight / hp, 1 / 3)).toFixed(3);
    },
    
    // Trap Speed (MPH) formula
    trapSpeed(weight, hp) {
        if (!weight || !hp || hp <= 0) return 0;
        return (234 * Math.pow(hp / weight, 1 / 3)).toFixed(2);
    }
};