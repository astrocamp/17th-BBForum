import Alpine from "alpinejs";

Alpine.data("stock_search", () => ({
    query: '',
    suggestions: [],
    selectedStockCode: null, 
    searchStocks() {
        if (this.query.length > 0) {
            fetch(`/search/?q=${this.query}`)
                .then(response => response.json())
                .then(data => {
                    this.suggestions = data.slice(0, 5);  
                });
        } else {
            this.suggestions = [];
        }
    },
    selectStock(securityCode, name) {
        this.query = name;  // 保留用户输入的名称
        this.suggestions = [];  
        this.selectedStockCode = securityCode; 
    },
    navigateToStock() {
        const matchedStock = this.suggestions.find(suggestion => 
            suggestion.name === this.query || suggestion.security_code === this.query
        );
        const securityCode = matchedStock ? matchedStock.security_code : this.selectedStockCode; 
        if (securityCode) {
            window.location.href = `/stocks/${securityCode}`;
        }
    }
}));
