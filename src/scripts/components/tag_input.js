import Alpine from "alpinejs";


Alpine.data("tagInput", () => ({
  tagify: null,

  init() {
    const input = this.$refs.tagInput;

    if (!input) {
      console.error("Input element not found");
      return;
    }

    this.tagify = new Tagify(input, {
      whitelist: [],
      enforceWhitelist: true,
      maxTags: 10,
      dropdown: {
        enabled: 1,
        maxItems: 10,
        closeOnSelect: false,
        fuzzySearch: true,
      }
    });

    this.loadWhitelist();

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (input.value.trim()) {
          this.tagify.addTags([input.value.trim()]);
          input.value = '';
        }
      }
    });

    input.addEventListener('input', () => {
      this.fetchSuggestions();
    });
  },

  async loadWhitelist() {
    try {
      const response = await fetch(`/articles/stocks_list/`);
      if (response.ok) {
        const text = await response.text();

        const stocks = JSON.parse(text);


        if (this.tagify) {
          this.tagify.settings.whitelist = stocks.map(stock => ({
            value: stock.value,
            id: stock.id
          }));
        }
      } else {
        console.error("Failed to load whitelist: ", response.statusText);
      }
    } catch (error) {
      console.error("Error loading whitelist:", error);
    }
  },
}));