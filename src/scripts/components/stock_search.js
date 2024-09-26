import Alpine from "alpinejs";

Alpine.data("stock_search", () => ({
    query: '',
    suggestions: [],
    selectedStockCode: null,
    securityCode: 0,
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
        this.query = securityCode;
        this.suggestions = [];
        this.selectedStockCode = securityCode;
    },
    navigateToStock(stockCode) {
        const matchedStock = this.suggestions.find(suggestion =>
            suggestion.name === this.query || suggestion.security_code === this.query
        );

        if (matchedStock) {

            this.securityCode = matchedStock.security_code;
        } else {

            if (/^[0-9]+$/.test(stockCode)) {
                this.securityCode = stockCode;
            } else {
                this.securityCode = 0;
            }
        }

        if (!this.securityCode || this.securityCode === 0) {
            window.location.href = '/stock_notfound/';
        } else {
            fetch(`/stocks/${this.securityCode}`)
            .then(response => {
                if (response.ok) {
                    window.location.href = `/stocks/${this.securityCode}`;
                } else {
                    window.location.href = '/stock_notfound/';
                }
            });
        }
    }
}));