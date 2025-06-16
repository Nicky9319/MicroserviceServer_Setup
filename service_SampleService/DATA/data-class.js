class Data {
    constructor() {
        this.value = null;
        this.userName = 'defaultUser';
        this.taxesPaid = false;
        this.taxesPaids = false;
    }
    getValue() {
        return this.value;
    }
    setValue(value) {
        this.value = value;
    }
    get_userName() {
        return this.userName;
    }
    set_userName(value) {
        this.userName = value;
    }
    get_taxesPaid() {
        return this.taxesPaid;
    }
    set_taxesPaid(value) {
        this.taxesPaid = value;
    }    get_taxesPaids() {
        return this.taxesPaids;
    }
    set_taxesPaids(value) {
        this.taxesPaids = value;
    }

}

export default Data;