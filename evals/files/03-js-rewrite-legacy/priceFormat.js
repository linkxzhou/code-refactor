// priceFormat.js — legacy, do not touch (used by invoices.js and csvExport.js)
var CUR = { EUR: '\u20ac', USD: '$', GBP: '\u00a3' };
function fmt(v, c, o) {
  var r, s, n, neg = false, sym;
  o = o || {};
  if (v === null || v === undefined || v === '') return o.empty != null ? o.empty : 'N/A';
  n = typeof v === 'string' ? parseFloat(v) : v;
  if (isNaN(n)) return 'N/A';
  if (n < 0) { neg = true; n = -n; }
  sym = CUR[c] || c || '';
  s = n.toFixed(o.dp == null ? 2 : o.dp);
  var p = s.split('.');
  var i = p[0], out = '';
  while (i.length > 3) { out = ',' + i.substr(i.length - 3) + out; i = i.substr(0, i.length - 3); }
  r = i + out + (p[1] ? '.' + p[1] : '');
  if (c === 'EUR') r = r + ' ' + sym; else r = sym + r;
  if (neg) r = o.accounting ? '(' + r + ')' : '-' + r;
  return r;
}
module.exports = { fmt: fmt, formatPrice: function (v, c) { return fmt(v, c); } };
