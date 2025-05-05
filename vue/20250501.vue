let dateObj = new Date(this.date.slice(0,4), this.date.slice(4,6)-1, this.date.slice(6,8));
dateObj.setDate(dateObj.getDate() - 1);
let result = dateObj.toISOString().slice(0,10).replace(/-/g, '');