import { Component, useState } from "@odoo/owl";

class Counter extends Component {
    static template = "property_rental.Counter";

    setup() {
        state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
}