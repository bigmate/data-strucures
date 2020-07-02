class Heap {
    constructor(length) {
        this._arr = new Array(length + 1);
        this._cap = length;
        this._len = 0;
    }

    get cap() {
        return this._cap;
    }

    get len() {
        return this._len;
    }

    set len(k) {
        if (k < 0) return;
        this._len = k;
    }

    insert(val) {
        if (this.len >= this.cap) throw new Error("Heap overflow");
        this.len++;
        this._arr[this._len] = val;
        this.swim(this._len);
    }

    delMax() {
        switch (this.len) {
            case 0:
                return;
            case 1:
                this.len--;
                return;
        }
        this.exchange(1, this.len);
        this.len--;
        this.sink(1);
    }

    swim(k) {
        while (k > 1 && !this.leParent(k)) {
            const parentIndex = Math.floor(k / 2);
            this.exchange(parentIndex, k);
            k = parentIndex;
        }
    }

    exchange(i, j) {
        const tmp = this._arr[i];
        this._arr[i] = this._arr[j];
        this._arr[j] = tmp;
    }

    sink(k) {
        let left = k * 2;
        let right = left + 1;
        while (k < this.len) {
            let max;
            if (left <= this.len && right <= this.len) {
                if (this._arr[k] > this._arr[left] && this._arr[k] > this._arr[right]) break;
                max = this._arr[left] > this._arr[right] ? left : right;
            } else if (left <= this.len) {
                if (this._arr[k] > this._arr[left]) break;
                max = left;
            } else {
                break;
            }
            this.exchange(k, max);
            k = max;
            left = max * 2;
            right = left + 1;
        }
    }

    leParent(k) {
        return this._arr[Math.floor(k / 2)] > this._arr[k];
    }

    toString() {
        return "[" + this._arr.slice(1).join(", ") + "]";
    }

    sort() {
        while (this.len > 1) {
            this.delMax()
        }
    }
}

export { Heap };
