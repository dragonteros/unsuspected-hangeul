!function(t){var e={};function r(n){if(e[n])return e[n].exports;var o=e[n]={i:n,l:!1,exports:{}};return t[n].call(o.exports,o,o.exports,r),o.l=!0,o.exports}r.m=t,r.c=e,r.d=function(t,e,n){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},r.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var o in t)r.d(n,o,function(e){return t[e]}.bind(null,o));return n},r.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="",r(r.s=2)}([function(t,e,r){(function(t){var r,n=function(t){"use strict";var e=1e7,r=7,o=9007199254740992,i=h(o),u="0123456789abcdefghijklmnopqrstuvwxyz",a="function"==typeof BigInt;function s(t,e,r,n){return void 0===t?s[0]:void 0!==e&&(10!=+e||r)?F(t,e,r,n):H(t)}function p(t,e){this.value=t,this.sign=e,this.isSmall=!1}function l(t){this.value=t,this.sign=t<0,this.isSmall=!0}function f(t){this.value=t}function c(t){return-o<t&&t<o}function h(t){return t<1e7?[t]:t<1e14?[t%1e7,Math.floor(t/1e7)]:[t%1e7,Math.floor(t/1e7)%1e7,Math.floor(t/1e14)]}function v(t){y(t);var r=t.length;if(r<4&&P(t,i)<0)switch(r){case 0:return 0;case 1:return t[0];case 2:return t[0]+t[1]*e;default:return t[0]+(t[1]+t[2]*e)*e}return t}function y(t){for(var e=t.length;0===t[--e];);t.length=e+1}function g(t){for(var e=new Array(t),r=-1;++r<t;)e[r]=0;return e}function m(t){return t>0?Math.floor(t):Math.ceil(t)}function d(t,r){var n,o,i=t.length,u=r.length,a=new Array(i),s=0,p=e;for(o=0;o<u;o++)s=(n=t[o]+r[o]+s)>=p?1:0,a[o]=n-s*p;for(;o<i;)s=(n=t[o]+s)===p?1:0,a[o++]=n-s*p;return s>0&&a.push(s),a}function w(t,e){return t.length>=e.length?d(t,e):d(e,t)}function b(t,r){var n,o,i=t.length,u=new Array(i),a=e;for(o=0;o<i;o++)n=t[o]-a+r,r=Math.floor(n/a),u[o]=n-r*a,r+=1;for(;r>0;)u[o++]=r%a,r=Math.floor(r/a);return u}function E(t,r){var n,o,i=t.length,u=r.length,a=new Array(i),s=0,p=e;for(n=0;n<u;n++)(o=t[n]-s-r[n])<0?(o+=p,s=1):s=0,a[n]=o;for(n=u;n<i;n++){if(!((o=t[n]-s)<0)){a[n++]=o;break}o+=p,a[n]=o}for(;n<i;n++)a[n]=t[n];return y(a),a}function S(t,r,n){var o,i,u=t.length,a=new Array(u),s=-r,f=e;for(o=0;o<u;o++)i=t[o]+s,s=Math.floor(i/f),i%=f,a[o]=i<0?i+f:i;return"number"==typeof(a=v(a))?(n&&(a=-a),new l(a)):new p(a,n)}function x(t,r){var n,o,i,u,a=t.length,s=r.length,p=g(a+s),l=e;for(i=0;i<a;++i){u=t[i];for(var f=0;f<s;++f)n=u*r[f]+p[i+f],o=Math.floor(n/l),p[i+f]=n-o*l,p[i+f+1]+=o}return y(p),p}function N(t,r){var n,o,i=t.length,u=new Array(i),a=e,s=0;for(o=0;o<i;o++)n=t[o]*r+s,s=Math.floor(n/a),u[o]=n-s*a;for(;s>0;)u[o++]=s%a,s=Math.floor(s/a);return u}function M(t,e){for(var r=[];e-- >0;)r.push(0);return r.concat(t)}function O(t,r,n){return new p(t<e?N(r,t):x(r,h(t)),n)}function q(t){var r,n,o,i,u=t.length,a=g(u+u),s=e;for(o=0;o<u;o++){n=0-(i=t[o])*i;for(var p=o;p<u;p++)r=i*t[p]*2+a[o+p]+n,n=Math.floor(r/s),a[o+p]=r-n*s;a[o+u]=n}return y(a),a}function A(t,r){var n,o,i,u,a=t.length,s=g(a),p=e;for(i=0,n=a-1;n>=0;--n)i=(u=i*p+t[n])-(o=m(u/r))*r,s[n]=0|o;return[s,0|i]}function B(t,r){var n,o=H(r);if(a)return[new f(t.value/o.value),new f(t.value%o.value)];var i,u=t.value,c=o.value;if(0===c)throw new Error("Cannot divide by zero");if(t.isSmall)return o.isSmall?[new l(m(u/c)),new l(u%c)]:[s[0],t];if(o.isSmall){if(1===c)return[t,s[0]];if(-1==c)return[t.negate(),s[0]];var d=Math.abs(c);if(d<e){i=v((n=A(u,d))[0]);var w=n[1];return t.sign&&(w=-w),"number"==typeof i?(t.sign!==o.sign&&(i=-i),[new l(i),new l(w)]):[new p(i,t.sign!==o.sign),new l(w)]}c=h(d)}var b=P(u,c);if(-1===b)return[s[0],t];if(0===b)return[s[t.sign===o.sign?1:-1],s[0]];i=(n=u.length+c.length<=200?function(t,r){var n,o,i,u,a,s,p,l=t.length,f=r.length,c=e,h=g(r.length),y=r[f-1],m=Math.ceil(c/(2*y)),d=N(t,m),w=N(r,m);for(d.length<=l&&d.push(0),w.push(0),y=w[f-1],o=l-f;o>=0;o--){for(n=c-1,d[o+f]!==y&&(n=Math.floor((d[o+f]*c+d[o+f-1])/y)),i=0,u=0,s=w.length,a=0;a<s;a++)i+=n*w[a],p=Math.floor(i/c),u+=d[o+a]-(i-p*c),i=p,u<0?(d[o+a]=u+c,u=-1):(d[o+a]=u,u=0);for(;0!==u;){for(n-=1,i=0,a=0;a<s;a++)(i+=d[o+a]-c+w[a])<0?(d[o+a]=i+c,i=0):(d[o+a]=i,i=1);u+=i}h[o]=n}return d=A(d,m)[0],[v(h),v(d)]}(u,c):function(t,r){for(var n,o,i,u,a,s=t.length,p=r.length,l=[],f=[],c=e;s;)if(f.unshift(t[--s]),y(f),P(f,r)<0)l.push(0);else{i=f[(o=f.length)-1]*c+f[o-2],u=r[p-1]*c+r[p-2],o>p&&(i=(i+1)*c),n=Math.ceil(i/u);do{if(P(a=N(r,n),f)<=0)break;n--}while(n);l.push(n),f=E(f,a)}return l.reverse(),[v(l),v(f)]}(u,c))[0];var S=t.sign!==o.sign,x=n[1],M=t.sign;return"number"==typeof i?(S&&(i=-i),i=new l(i)):i=new p(i,S),"number"==typeof x?(M&&(x=-x),x=new l(x)):x=new p(x,M),[i,x]}function P(t,e){if(t.length!==e.length)return t.length>e.length?1:-1;for(var r=t.length-1;r>=0;r--)if(t[r]!==e[r])return t[r]>e[r]?1:-1;return 0}function j(t){var e=t.abs();return!e.isUnit()&&(!!(e.equals(2)||e.equals(3)||e.equals(5))||!(e.isEven()||e.isDivisibleBy(3)||e.isDivisibleBy(5))&&(!!e.lesser(49)||void 0))}function I(t,e){for(var r,o,i,u=t.prev(),a=u,s=0;a.isEven();)a=a.divide(2),s++;t:for(o=0;o<e.length;o++)if(!t.lesser(e[o])&&!(i=n(e[o]).modPow(a,t)).isUnit()&&!i.equals(u)){for(r=s-1;0!=r;r--){if((i=i.square().mod(t)).isUnit())return!1;if(i.equals(u))continue t}return!1}return!0}p.prototype=Object.create(s.prototype),l.prototype=Object.create(s.prototype),f.prototype=Object.create(s.prototype),p.prototype.add=function(t){var e=H(t);if(this.sign!==e.sign)return this.subtract(e.negate());var r=this.value,n=e.value;return e.isSmall?new p(b(r,Math.abs(n)),this.sign):new p(w(r,n),this.sign)},p.prototype.plus=p.prototype.add,l.prototype.add=function(t){var e=H(t),r=this.value;if(r<0!==e.sign)return this.subtract(e.negate());var n=e.value;if(e.isSmall){if(c(r+n))return new l(r+n);n=h(Math.abs(n))}return new p(b(n,Math.abs(r)),r<0)},l.prototype.plus=l.prototype.add,f.prototype.add=function(t){return new f(this.value+H(t).value)},f.prototype.plus=f.prototype.add,p.prototype.subtract=function(t){var e=H(t);if(this.sign!==e.sign)return this.add(e.negate());var r=this.value,n=e.value;return e.isSmall?S(r,Math.abs(n),this.sign):function(t,e,r){var n;return P(t,e)>=0?n=E(t,e):(n=E(e,t),r=!r),"number"==typeof(n=v(n))?(r&&(n=-n),new l(n)):new p(n,r)}(r,n,this.sign)},p.prototype.minus=p.prototype.subtract,l.prototype.subtract=function(t){var e=H(t),r=this.value;if(r<0!==e.sign)return this.add(e.negate());var n=e.value;return e.isSmall?new l(r-n):S(n,Math.abs(r),r>=0)},l.prototype.minus=l.prototype.subtract,f.prototype.subtract=function(t){return new f(this.value-H(t).value)},f.prototype.minus=f.prototype.subtract,p.prototype.negate=function(){return new p(this.value,!this.sign)},l.prototype.negate=function(){var t=this.sign,e=new l(-this.value);return e.sign=!t,e},f.prototype.negate=function(){return new f(-this.value)},p.prototype.abs=function(){return new p(this.value,!1)},l.prototype.abs=function(){return new l(Math.abs(this.value))},f.prototype.abs=function(){return new f(this.value>=0?this.value:-this.value)},p.prototype.multiply=function(t){var r,n,o,i=H(t),u=this.value,a=i.value,l=this.sign!==i.sign;if(i.isSmall){if(0===a)return s[0];if(1===a)return this;if(-1===a)return this.negate();if((r=Math.abs(a))<e)return new p(N(u,r),l);a=h(r)}return n=u.length,o=a.length,new p(-.012*n-.012*o+15e-6*n*o>0?function t(e,r){var n=Math.max(e.length,r.length);if(n<=30)return x(e,r);n=Math.ceil(n/2);var o=e.slice(n),i=e.slice(0,n),u=r.slice(n),a=r.slice(0,n),s=t(i,a),p=t(o,u),l=t(w(i,o),w(a,u)),f=w(w(s,M(E(E(l,s),p),n)),M(p,2*n));return y(f),f}(u,a):x(u,a),l)},p.prototype.times=p.prototype.multiply,l.prototype._multiplyBySmall=function(t){return c(t.value*this.value)?new l(t.value*this.value):O(Math.abs(t.value),h(Math.abs(this.value)),this.sign!==t.sign)},p.prototype._multiplyBySmall=function(t){return 0===t.value?s[0]:1===t.value?this:-1===t.value?this.negate():O(Math.abs(t.value),this.value,this.sign!==t.sign)},l.prototype.multiply=function(t){return H(t)._multiplyBySmall(this)},l.prototype.times=l.prototype.multiply,f.prototype.multiply=function(t){return new f(this.value*H(t).value)},f.prototype.times=f.prototype.multiply,p.prototype.square=function(){return new p(q(this.value),!1)},l.prototype.square=function(){var t=this.value*this.value;return c(t)?new l(t):new p(q(h(Math.abs(this.value))),!1)},f.prototype.square=function(t){return new f(this.value*this.value)},p.prototype.divmod=function(t){var e=B(this,t);return{quotient:e[0],remainder:e[1]}},f.prototype.divmod=l.prototype.divmod=p.prototype.divmod,p.prototype.divide=function(t){return B(this,t)[0]},f.prototype.over=f.prototype.divide=function(t){return new f(this.value/H(t).value)},l.prototype.over=l.prototype.divide=p.prototype.over=p.prototype.divide,p.prototype.mod=function(t){return B(this,t)[1]},f.prototype.mod=f.prototype.remainder=function(t){return new f(this.value%H(t).value)},l.prototype.remainder=l.prototype.mod=p.prototype.remainder=p.prototype.mod,p.prototype.pow=function(t){var e,r,n,o=H(t),i=this.value,u=o.value;if(0===u)return s[1];if(0===i)return s[0];if(1===i)return s[1];if(-1===i)return o.isEven()?s[1]:s[-1];if(o.sign)return s[0];if(!o.isSmall)throw new Error("The exponent "+o.toString()+" is too large.");if(this.isSmall&&c(e=Math.pow(i,u)))return new l(m(e));for(r=this,n=s[1];!0&u&&(n=n.times(r),--u),0!==u;)u/=2,r=r.square();return n},l.prototype.pow=p.prototype.pow,f.prototype.pow=function(t){var e=H(t),r=this.value,n=e.value,o=BigInt(0),i=BigInt(1),u=BigInt(2);if(n===o)return s[1];if(r===o)return s[0];if(r===i)return s[1];if(r===BigInt(-1))return e.isEven()?s[1]:s[-1];if(e.isNegative())return new f(o);for(var a=this,p=s[1];(n&i)===i&&(p=p.times(a),--n),n!==o;)n/=u,a=a.square();return p},p.prototype.modPow=function(t,e){if(t=H(t),(e=H(e)).isZero())throw new Error("Cannot take modPow with modulus 0");var r=s[1],n=this.mod(e);for(t.isNegative()&&(t=t.multiply(s[-1]),n=n.modInv(e));t.isPositive();){if(n.isZero())return s[0];t.isOdd()&&(r=r.multiply(n).mod(e)),t=t.divide(2),n=n.square().mod(e)}return r},f.prototype.modPow=l.prototype.modPow=p.prototype.modPow,p.prototype.compareAbs=function(t){var e=H(t),r=this.value,n=e.value;return e.isSmall?1:P(r,n)},l.prototype.compareAbs=function(t){var e=H(t),r=Math.abs(this.value),n=e.value;return e.isSmall?r===(n=Math.abs(n))?0:r>n?1:-1:-1},f.prototype.compareAbs=function(t){var e=this.value,r=H(t).value;return(e=e>=0?e:-e)===(r=r>=0?r:-r)?0:e>r?1:-1},p.prototype.compare=function(t){if(t===1/0)return-1;if(t===-1/0)return 1;var e=H(t),r=this.value,n=e.value;return this.sign!==e.sign?e.sign?1:-1:e.isSmall?this.sign?-1:1:P(r,n)*(this.sign?-1:1)},p.prototype.compareTo=p.prototype.compare,l.prototype.compare=function(t){if(t===1/0)return-1;if(t===-1/0)return 1;var e=H(t),r=this.value,n=e.value;return e.isSmall?r==n?0:r>n?1:-1:r<0!==e.sign?r<0?-1:1:r<0?1:-1},l.prototype.compareTo=l.prototype.compare,f.prototype.compare=function(t){if(t===1/0)return-1;if(t===-1/0)return 1;var e=this.value,r=H(t).value;return e===r?0:e>r?1:-1},f.prototype.compareTo=f.prototype.compare,p.prototype.equals=function(t){return 0===this.compare(t)},f.prototype.eq=f.prototype.equals=l.prototype.eq=l.prototype.equals=p.prototype.eq=p.prototype.equals,p.prototype.notEquals=function(t){return 0!==this.compare(t)},f.prototype.neq=f.prototype.notEquals=l.prototype.neq=l.prototype.notEquals=p.prototype.neq=p.prototype.notEquals,p.prototype.greater=function(t){return this.compare(t)>0},f.prototype.gt=f.prototype.greater=l.prototype.gt=l.prototype.greater=p.prototype.gt=p.prototype.greater,p.prototype.lesser=function(t){return this.compare(t)<0},f.prototype.lt=f.prototype.lesser=l.prototype.lt=l.prototype.lesser=p.prototype.lt=p.prototype.lesser,p.prototype.greaterOrEquals=function(t){return this.compare(t)>=0},f.prototype.geq=f.prototype.greaterOrEquals=l.prototype.geq=l.prototype.greaterOrEquals=p.prototype.geq=p.prototype.greaterOrEquals,p.prototype.lesserOrEquals=function(t){return this.compare(t)<=0},f.prototype.leq=f.prototype.lesserOrEquals=l.prototype.leq=l.prototype.lesserOrEquals=p.prototype.leq=p.prototype.lesserOrEquals,p.prototype.isEven=function(){return 0==(1&this.value[0])},l.prototype.isEven=function(){return 0==(1&this.value)},f.prototype.isEven=function(){return(this.value&BigInt(1))===BigInt(0)},p.prototype.isOdd=function(){return 1==(1&this.value[0])},l.prototype.isOdd=function(){return 1==(1&this.value)},f.prototype.isOdd=function(){return(this.value&BigInt(1))===BigInt(1)},p.prototype.isPositive=function(){return!this.sign},l.prototype.isPositive=function(){return this.value>0},f.prototype.isPositive=l.prototype.isPositive,p.prototype.isNegative=function(){return this.sign},l.prototype.isNegative=function(){return this.value<0},f.prototype.isNegative=l.prototype.isNegative,p.prototype.isUnit=function(){return!1},l.prototype.isUnit=function(){return 1===Math.abs(this.value)},f.prototype.isUnit=function(){return this.abs().value===BigInt(1)},p.prototype.isZero=function(){return!1},l.prototype.isZero=function(){return 0===this.value},f.prototype.isZero=function(){return this.value===BigInt(0)},p.prototype.isDivisibleBy=function(t){var e=H(t);return!e.isZero()&&(!!e.isUnit()||(0===e.compareAbs(2)?this.isEven():this.mod(e).isZero()))},f.prototype.isDivisibleBy=l.prototype.isDivisibleBy=p.prototype.isDivisibleBy,p.prototype.isPrime=function(t){var e=j(this);if(void 0!==e)return e;var r=this.abs(),o=r.bitLength();if(o<=64)return I(r,[2,3,5,7,11,13,17,19,23,29,31,37]);for(var i=Math.log(2)*o.toJSNumber(),u=Math.ceil(!0===t?2*Math.pow(i,2):i),a=[],s=0;s<u;s++)a.push(n(s+2));return I(r,a)},f.prototype.isPrime=l.prototype.isPrime=p.prototype.isPrime,p.prototype.isProbablePrime=function(t){var e=j(this);if(void 0!==e)return e;for(var r=this.abs(),o=void 0===t?5:t,i=[],u=0;u<o;u++)i.push(n.randBetween(2,r.minus(2)));return I(r,i)},f.prototype.isProbablePrime=l.prototype.isProbablePrime=p.prototype.isProbablePrime,p.prototype.modInv=function(t){for(var e,r,o,i=n.zero,u=n.one,a=H(t),s=this.abs();!s.isZero();)e=a.divide(s),r=i,o=a,i=u,a=s,u=r.subtract(e.multiply(u)),s=o.subtract(e.multiply(s));if(!a.isUnit())throw new Error(this.toString()+" and "+t.toString()+" are not co-prime");return-1===i.compare(0)&&(i=i.add(t)),this.isNegative()?i.negate():i},f.prototype.modInv=l.prototype.modInv=p.prototype.modInv,p.prototype.next=function(){var t=this.value;return this.sign?S(t,1,this.sign):new p(b(t,1),this.sign)},l.prototype.next=function(){var t=this.value;return t+1<o?new l(t+1):new p(i,!1)},f.prototype.next=function(){return new f(this.value+BigInt(1))},p.prototype.prev=function(){var t=this.value;return this.sign?new p(b(t,1),!0):S(t,1,this.sign)},l.prototype.prev=function(){var t=this.value;return t-1>-o?new l(t-1):new p(i,!0)},f.prototype.prev=function(){return new f(this.value-BigInt(1))};for(var U=[1];2*U[U.length-1]<=e;)U.push(2*U[U.length-1]);var C=U.length,L=U[C-1];function J(t){return Math.abs(t)<=e}function _(t,e,r){e=H(e);for(var o=t.isNegative(),i=e.isNegative(),u=o?t.not():t,a=i?e.not():e,s=0,p=0,l=null,f=null,c=[];!u.isZero()||!a.isZero();)s=(l=B(u,L))[1].toJSNumber(),o&&(s=L-1-s),p=(f=B(a,L))[1].toJSNumber(),i&&(p=L-1-p),u=l[0],a=f[0],c.push(r(s,p));for(var h=0!==r(o?1:0,i?1:0)?n(-1):n(0),v=c.length-1;v>=0;v-=1)h=h.multiply(L).add(n(c[v]));return h}p.prototype.shiftLeft=function(t){var e=H(t).toJSNumber();if(!J(e))throw new Error(String(e)+" is too large for shifting.");if(e<0)return this.shiftRight(-e);var r=this;if(r.isZero())return r;for(;e>=C;)r=r.multiply(L),e-=C-1;return r.multiply(U[e])},f.prototype.shiftLeft=l.prototype.shiftLeft=p.prototype.shiftLeft,p.prototype.shiftRight=function(t){var e,r=H(t).toJSNumber();if(!J(r))throw new Error(String(r)+" is too large for shifting.");if(r<0)return this.shiftLeft(-r);for(var n=this;r>=C;){if(n.isZero()||n.isNegative()&&n.isUnit())return n;n=(e=B(n,L))[1].isNegative()?e[0].prev():e[0],r-=C-1}return(e=B(n,U[r]))[1].isNegative()?e[0].prev():e[0]},f.prototype.shiftRight=l.prototype.shiftRight=p.prototype.shiftRight,p.prototype.not=function(){return this.negate().prev()},f.prototype.not=l.prototype.not=p.prototype.not,p.prototype.and=function(t){return _(this,t,(function(t,e){return t&e}))},f.prototype.and=l.prototype.and=p.prototype.and,p.prototype.or=function(t){return _(this,t,(function(t,e){return t|e}))},f.prototype.or=l.prototype.or=p.prototype.or,p.prototype.xor=function(t){return _(this,t,(function(t,e){return t^e}))},f.prototype.xor=l.prototype.xor=p.prototype.xor;var Z=1<<30,k=(e&-e)*(e&-e)|Z;function T(t){var r=t.value,n="number"==typeof r?r|Z:"bigint"==typeof r?r|BigInt(Z):r[0]+r[1]*e|k;return n&-n}function D(t,e){return t=H(t),e=H(e),t.greater(e)?t:e}function R(t,e){return t=H(t),e=H(e),t.lesser(e)?t:e}function z(t,e){if(t=H(t).abs(),e=H(e).abs(),t.equals(e))return t;if(t.isZero())return e;if(e.isZero())return t;for(var r,n,o=s[1];t.isEven()&&e.isEven();)r=R(T(t),T(e)),t=t.divide(r),e=e.divide(r),o=o.multiply(r);for(;t.isEven();)t=t.divide(T(t));do{for(;e.isEven();)e=e.divide(T(e));t.greater(e)&&(n=e,e=t,t=n),e=e.subtract(t)}while(!e.isZero());return o.isUnit()?t:t.multiply(o)}p.prototype.bitLength=function(){var t=this;return t.compareTo(n(0))<0&&(t=t.negate().subtract(n(1))),0===t.compareTo(n(0))?n(0):n(function t(e,r){if(r.compareTo(e)<=0){var o=t(e,r.square(r)),i=o.p,u=o.e,a=i.multiply(r);return a.compareTo(e)<=0?{p:a,e:2*u+1}:{p:i,e:2*u}}return{p:n(1),e:0}}(t,n(2)).e).add(n(1))},f.prototype.bitLength=l.prototype.bitLength=p.prototype.bitLength;var F=function(t,e,r,n){r=r||u,t=String(t),n||(t=t.toLowerCase(),r=r.toLowerCase());var o,i=t.length,a=Math.abs(e),s={};for(o=0;o<r.length;o++)s[r[o]]=o;for(o=0;o<i;o++){if("-"!==(f=t[o])&&(f in s&&s[f]>=a)){if("1"===f&&1===a)continue;throw new Error(f+" is not a valid digit in base "+e+".")}}e=H(e);var p=[],l="-"===t[0];for(o=l?1:0;o<t.length;o++){var f;if((f=t[o])in s)p.push(H(s[f]));else{if("<"!==f)throw new Error(f+" is not a valid character");var c=o;do{o++}while(">"!==t[o]&&o<t.length);p.push(H(t.slice(c+1,o)))}}return V(p,e,l)};function V(t,e,r){var n,o=s[0],i=s[1];for(n=t.length-1;n>=0;n--)o=o.add(t[n].times(i)),i=i.times(e);return r?o.negate():o}function $(t,e){if((e=n(e)).isZero()){if(t.isZero())return{value:[0],isNegative:!1};throw new Error("Cannot convert nonzero numbers to base 0.")}if(e.equals(-1)){if(t.isZero())return{value:[0],isNegative:!1};if(t.isNegative())return{value:[].concat.apply([],Array.apply(null,Array(-t.toJSNumber())).map(Array.prototype.valueOf,[1,0])),isNegative:!1};var r=Array.apply(null,Array(t.toJSNumber()-1)).map(Array.prototype.valueOf,[0,1]);return r.unshift([1]),{value:[].concat.apply([],r),isNegative:!1}}var o=!1;if(t.isNegative()&&e.isPositive()&&(o=!0,t=t.abs()),e.isUnit())return t.isZero()?{value:[0],isNegative:!1}:{value:Array.apply(null,Array(t.toJSNumber())).map(Number.prototype.valueOf,1),isNegative:o};for(var i,u=[],a=t;a.isNegative()||a.compareAbs(e)>=0;){i=a.divmod(e),a=i.quotient;var s=i.remainder;s.isNegative()&&(s=e.minus(s).abs(),a=a.next()),u.push(s.toJSNumber())}return u.push(a.toJSNumber()),{value:u.reverse(),isNegative:o}}function K(t,e,r){var n=$(t,e);return(n.isNegative?"-":"")+n.value.map((function(t){return function(t,e){return t<(e=e||u).length?e[t]:"<"+t+">"}(t,r)})).join("")}function G(t){if(c(+t)){var e=+t;if(e===m(e))return a?new f(BigInt(e)):new l(e);throw new Error("Invalid integer: "+t)}var n="-"===t[0];n&&(t=t.slice(1));var o=t.split(/e/i);if(o.length>2)throw new Error("Invalid integer: "+o.join("e"));if(2===o.length){var i=o[1];if("+"===i[0]&&(i=i.slice(1)),(i=+i)!==m(i)||!c(i))throw new Error("Invalid integer: "+i+" is not a valid exponent.");var u=o[0],s=u.indexOf(".");if(s>=0&&(i-=u.length-s-1,u=u.slice(0,s)+u.slice(s+1)),i<0)throw new Error("Cannot include negative exponent part for integers");t=u+=new Array(i+1).join("0")}if(!/^([0-9][0-9]*)$/.test(t))throw new Error("Invalid integer: "+t);if(a)return new f(BigInt(n?"-"+t:t));for(var h=[],v=t.length,g=r,d=v-g;v>0;)h.push(+t.slice(d,v)),(d-=g)<0&&(d=0),v-=g;return y(h),new p(h,n)}function H(t){return"number"==typeof t?function(t){if(a)return new f(BigInt(t));if(c(t)){if(t!==m(t))throw new Error(t+" is not an integer.");return new l(t)}return G(t.toString())}(t):"string"==typeof t?G(t):"bigint"==typeof t?new f(t):t}p.prototype.toArray=function(t){return $(this,t)},l.prototype.toArray=function(t){return $(this,t)},f.prototype.toArray=function(t){return $(this,t)},p.prototype.toString=function(t,e){if(void 0===t&&(t=10),10!==t)return K(this,t,e);for(var r,n=this.value,o=n.length,i=String(n[--o]);--o>=0;)r=String(n[o]),i+="0000000".slice(r.length)+r;return(this.sign?"-":"")+i},l.prototype.toString=function(t,e){return void 0===t&&(t=10),10!=t?K(this,t,e):String(this.value)},f.prototype.toString=l.prototype.toString,f.prototype.toJSON=p.prototype.toJSON=l.prototype.toJSON=function(){return this.toString()},p.prototype.valueOf=function(){return parseInt(this.toString(),10)},p.prototype.toJSNumber=p.prototype.valueOf,l.prototype.valueOf=function(){return this.value},l.prototype.toJSNumber=l.prototype.valueOf,f.prototype.valueOf=f.prototype.toJSNumber=function(){return parseInt(this.toString(),10)};for(var Q=0;Q<1e3;Q++)s[Q]=H(Q),Q>0&&(s[-Q]=H(-Q));return s.one=s[1],s.zero=s[0],s.minusOne=s[-1],s.max=D,s.min=R,s.gcd=z,s.lcm=function(t,e){return t=H(t).abs(),e=H(e).abs(),t.divide(z(t,e)).multiply(e)},s.isInstance=function(t){return t instanceof p||t instanceof l||t instanceof f},s.randBetween=function(t,r){var n=R(t=H(t),r=H(r)),o=D(t,r).subtract(n).add(1);if(o.isSmall)return n.add(Math.floor(Math.random()*o));for(var i=$(o,e).value,u=[],a=!0,p=0;p<i.length;p++){var l=a?i[p]:e,f=m(Math.random()*l);u.push(f),f<l&&(a=!1)}return n.add(s.fromArray(u,e,!1))},s.fromArray=function(t,e,r){return V(t.map(H),H(e||10),r)},s}();t.hasOwnProperty("exports")&&(t.exports=n),void 0===(r=function(){return n}.apply(e,[]))||(t.exports=r)}).call(this,r(1)(t))},function(t,e){t.exports=function(t){return t.webpackPolyfill||(t.deprecate=function(){},t.paths=[],t.children||(t.children=[]),Object.defineProperty(t,"loaded",{enumerable:!0,get:function(){return t.l}}),Object.defineProperty(t,"id",{enumerable:!0,get:function(){return t.i}}),t.webpackPolyfill=1),t}},function(t,e,r){"use strict";r.r(e);var n=r(0),o=r.n(n);function i(t){this.value=t}function u(t){this.rel=t}function a(t,e){this.relA=t,this.relF=e}function s(t){this.body=t}function p(t,e){this.fun=t,this.argv=e}function l(t,e,r){this.funs=t,this.args=e,this.utils=r}function f(t){this.value=t}function c(t){this.value=t}function h(t){this.value=t}function v(t){this.value=t}f.displayName="Number",c.displayName="Boolean",h.displayName="List",v.displayName="String";class y{constructor(t){this.value=t,this.str=null}formatByte(t){return"\\x"+("0"+(t=t.toString(16).toUpperCase())).slice(-2)}toString(){if(!this.str){const t=Array.from(new Uint8Array(this.value)).map(this.formatByte);this.str="b'"+t.join("")+"'"}return this.str}}y.displayName="Bytes";class g{constructor(t){this.value=t,this._keys=null,this._values=null}keys(){return this._keys||(this._keys=Object.keys(this.value).sort()),this._keys}values(){return this._values||(this._values=this._keys.map(t=>this.value[t])),this._values}}function m(t,e){this.inst=t,this.argv=e}function d(){}g.displayName="Dict",m.displayName="IO",d.displayName="Nil";var w=0;class b{constructor(t=""){this.id=w++,this.str="<"+t+"Function #"+this.id+">"}toString(){return this.str}}b.displayName="Function";class E extends b{constructor(t,e){super(),this.body=t,this.env=e,this.str="<Closure #"+this.id+" from depth "+this.env.args.length+">"}execute(t){const e=this.env.args.concat([t]),r=new l(this.env.funs,e,this.env.utils);return new x(this.body,r,null)}}class S extends b{constructor(t,e){super(),this.module=t,this.str="<Builtin Module "+e+">"}execute(t){return this.module(t)}}function x(t,e,r){this.expr=t,this.env=e,this.cache=r}const N=[b,c,h,g,v,y],M=[f,m,d].concat(N);function O(t){return t instanceof x&&t.expr instanceof i}function q(t){return t.value}function A(t,e){if((t=e(t))instanceof h)return new h(t.value.map(t=>A(t,e)));if(t instanceof g){const r=t.value,n={};return Object.keys(r).forEach((function(t){n[t]=A(r[t],e)})),new g(n)}return t}function B(t){return Array.isArray(t)?t:[t]}function P(t,e){return B(e).some((function(e){return B(t).every((function(t){return t instanceof e}))}))}function j(t){return t.length<2?t.toString():t.slice(0,-1).join(", ").concat(" and ",t[t.length-1])}function I(t,e){if(P(t=B(t),e=B(e)))return;const r=e.map(t=>t.displayName),n=t.map(t=>t.constructor.displayName);throw TypeError("Expected arguments of the same type among "+j(r)+" but received "+j(n))}function U(t,e){if(-1===(e=B(e)).indexOf(t.length))throw SyntaxError("Expected "+j(e)+" args but received "+t.length)}function C(t,e){if(!(t.length>=e))throw SyntaxError("Expected at least "+e+" args expected but received "+t.length)}function L(t,e,r,n){const o=t=>L(t,e,r,n);if(t=e(t),r&&t instanceof m)return t=r.doIO(t,r),t=o(t),n?"IO("+t+")":t;if(t instanceof f)return t.value.toString();if(t instanceof c)return t.value?"True":"False";if(t instanceof v)return"'"+t.value+"'";if(P(t,[y,b]))return t.toString();if(t instanceof h)return"["+t.value.map(o).join(", ")+"]";if(t instanceof g){return"{"+t.keys().map(e=>e+": "+o(t.value[e])).join(", ")+"}"}if(t instanceof m){const e=t.argv.map(o).join(",");return"<IO "+t.inst+" ("+e+")>"}if(t instanceof d)return"Nil";throw EvalError("Unexpected value: "+t)}const J=["ㄱ","ㄱ","ㄴ","ㄷ","ㄷ","ㄹ","ㅁ","ㅂ","ㅂ","ㅅ","ㅅ"," ㅇ","ㅈ","ㅈ","ㅈ","ㄱ","ㄷ","ㅂ"," ㅎ","ㄴㄱ","ㄴ","ㄴㄷ","ㄴㅂ","ㄷㄱ","ㄹㄴ","ㄹ","ㄹ ㅎ","ㄹ","ㅁㅂ","ㅁ","ㅂㄱ","ㅂㄴ","ㅂㄷ","ㅂㅅ","ㅂㅅㄱ","ㅂㅅㄷ","ㅂㅅㅂ","ㅂㅅ","ㅂㅅㅈ","ㅂㅈ","ㅂㅈ","ㅂㄷ","ㅂㅂ","ㅂ","ㅂ","ㅅㄱ","ㅅㄴ","ㅅㄷ","ㅅㄹ","ㅅㅁ","ㅅㅂ","ㅅㅂㄱ","ㅅㅅ","ㅅ ㅇ","ㅅㅈ","ㅅㅈ","ㅅㄱ","ㅅㄷ","ㅅㅂ","ㅅ ㅎ","ㅅ","ㅅ","ㅅ","ㅅ","ㅅ"," ㅇㄱ"," ㅇㄷ"," ㅇㅁ"," ㅇㅂ"," ㅇㅅ"," ㅇㅅ"," ㅇ"," ㅇㅈ"," ㅇㅈ"," ㅇㄷ"," ㅇㅂ"," ㅇ","ㅈ ㅇ","ㅈ","ㅈ","ㅈ","ㅈ","ㅈㄱ","ㅈ ㅎ","ㅈ","ㅈ","ㅂㅂ","ㅂ"," ㅎ"," ㅎ","ㄱㄷ","ㄴㅅ","ㄴㅈ","ㄴ ㅎ","ㄷㄹ"],_=["ㄱ","ㄱ","ㄱㅅ","ㄴ","ㄴㅈ","ㄴ ㅎ","ㄷ","ㄷ","ㄹ","ㄹㄱ","ㄹㅁ","ㄹㅂ","ㄹㅅ","ㄹㄷ","ㄹㅂ","ㄹ ㅎ","ㅁ","ㅂ","ㅂ","ㅂㅅ","ㅅ","ㅅ"," ㅇ","ㅈ","ㅈ","ㅈ","ㄱ","ㄷ","ㅂ"," ㅎ"],Z=["ㄴ","ㄴㄷ","ㄴㅅ","ㄴㅅ","ㄹㄱㅅ","ㄹㄷ","ㄹㅂㅅ","ㅁㅅ","ㅁ","ㅂㄱ","ㅂㄷ","ㅂㅅㄱ","ㅂㅅㄷ","ㅂㅈ","ㅂㄷ","ㅂ","ㅂ","ㅅㄱ","ㅅㄴ"," ㅇ"," ㅇ"," ㅇㅅ"," ㅇㅅ","ㅂ"," ㅎ"," ㅎ"],k=["ㄷㅁ","ㄷㅂ","ㄷㅅ","ㄷㅈ","ㄹㄱ","ㄹㄱ","ㄹㄷ","ㄹㄷ","ㄹㅁ","ㄹㅂ","ㄹㅂ","ㄹㅂ","ㄹㅅ","ㄹㅈ","ㄹㄱ","ㅁㄱ","ㅁㄷ","ㅁㅅ","ㅂㅅㄷ","ㅂㄱ","ㅂ ㅎ","ㅅㅂ"," ㅇㄹ"," ㅇ ㅎ","ㅈ ㅎ","ㄷ","ㅂ ㅎ"," ㅎㅅ"," ㅎ"];function T(t){if(1!==t.length)throw Error("[normalizeChar] Length of string should be 1, not "+t.length+": "+t);function e(e,r,n=1){var o=t.charCodeAt(0)-r.charCodeAt(0);return(o=Math.floor(o/n))>=0&&o<e.length?e[o]:""}return t>="ᄀ"&&t<="ᇿ"?e(J,"ᄀ"):t>="〮"&&t<="〯"?"":t>="ㄱ"&&t<="ㅤ"?e(_,"ㄱ"):t>="ㅥ"&&t<="ㆎ"?e(Z,"ㅥ"):t>="ꥠ"&&t<="ꥼ"?e(k,"ꥠ"):t>="가"&&t<="힯"?e(J,"가",588):t>="ힰ"&&t<="ퟆ"?"":t>="ퟋ"&&t<="ퟻ"?"":t>="ﾡ"&&t<="ﾾ"?e(_,"ﾡ"):"ￂￃￄￅￆￇￊￋￌￍￎￏￒￓￔￕￖￗￚￛￜ".indexOf(t)>=0?"":" "}function D(t){return t.split("").map(T).join("").trim()}function R(t){var e=t.split("").map((function(t){return"ㄱㄴㄷㄹㅁㅂㅅㅈ".indexOf(t)}));if(-1!==e.indexOf(-1))throw SyntaxError("Argument "+t+" has an unsupported character");var r=o()(e.reverse().join(""),8);return t.length%2==0&&(r=r.times(-1)),r}function z(t){var e=(t=o()(t)).isNegative(),r=(t=t.abs()).toArray(8).value.reverse(),n=r.map(t=>"ㄱㄴㄷㄹㅁㅂㅅㅈ"[t]).join("");return n.length%2==0!==e&&(n+="ㄱ"),n}function F(t,e){if(-1!==t.indexOf("ㅎ")){var r=t.slice(1);if(r){if((r=R(r).toJSNumber())<0)throw SyntaxError("Function call with negative number of arguments: "+r);var n=e.pop();if(0===r)e.push(new p(n,[]));else{var o=e.splice(-r,r);if(o.length<r)throw SyntaxError("Function call required "+r+" arguments but there are only "+o.length);e.push(new p(n,o))}}else{var l=e.pop();e.push(new s(l))}}else if(-1!==t.indexOf("ㅇ")){var f,c=t.slice(1);if(c){var h=e.pop();f=R(c).toJSNumber(),e.push(new a(h,f))}else{if(!((f=e.pop())instanceof i))throw SyntaxError("Function reference admits integer literals only, but received:"+f);f=f.value.toJSNumber(),e.push(new u(f))}}else e.push(new i(R(t)))}function V(t){for(var e=D(t).split(" "),r=[],n=e.length,o=0;o<n;o++)e[o]&&F(e[o],r);return r}class $ extends b{constructor(t){super("Piped "),this.funs=t}execute(t){return this.funs.reduce((t,e)=>[e(t)],t)[0]}}class K extends b{constructor(t,e){super("Collectedly-Receiving "),this.fn=t,this.strict=e}execute(t){U(t,1);const e=this.strict(t[0]);return I(e,h),this.fn(e.value)}}class G extends b{constructor(t){super("Spreadly-Receiving "),this.fn=t}execute(t){return this.fn([new h(t)])}}function H(t){return 0===t.length||t.every((function(e){return e===t[0]}))}const Q=["utf","unsigned","signed","float"];class W extends b{constructor(t,e,r,n){super(),this.strict=t,I([e,r],f),this.scheme=Q[e.value],this.numBytes=r.value,this.bigEndian=n&&n.value,this.codec=this.getCodec(),this.endianness="",void 0!==n&&(I(n,c),this.endianness=n.value?"big":"little"),this.str="<Codec(scheme="+this.scheme+", num_bytes="+this.numBytes+", big_endian="+this.bigEndian+")>"}execute(t){return t=t.map(this.strict),this.codec(...t)}getCodec(){switch(this.scheme){case"utf":return this.unicodeCodec;case"signed":case"unsigned":return this.integerCodec;case"float":return this.floatingPointCodec}}unicodeCodec(t){if(I(t,[v,y]),t instanceof v){var e=t.value;1==this.numBytes?e=unescape(encodeURIComponent(e)):""===this.endianness&&(e="\ufeff"+e);const r=e.split("").map(t=>t.charCodeAt(0)),n=new ArrayBuffer(r.length*this.numBytes);return function(t,e,r,n){const o={1:t.setUint8,2:t.setUint16,4:t.setUint32}[r].bind(t);for(let t=0;t<e.length;t++)o(t*r,e[t],!n)}(new DataView(n),r,this.numBytes,this.bigEndian),new y(n)}{const e=t.value;var r=new DataView(e),n=this.bigEndian||!1;if(""===this.endianness&&this.numBytes>1){const t=(this.numBytes>2?r.getUint32:r.getUint16).bind(r),o=65279===t(0);(o||65279===t(0,!0))&&(n=o,r=new DataView(e,this.numBytes))}var o=function(t,e,r){const n={1:t.getUint8,2:t.getUint16,4:t.getUint32}[e].bind(t);var o=[];for(let i=0;i<t.byteLength;i+=e)o.push(n(i,!r));return o}(r,this.numBytes,n).map(t=>String.fromCharCode(t)).join("");return 1==this.numBytes&&(o=decodeURIComponent(escape(o))),new v(o)}}integerCodec(t){const e="signed"===this.scheme;if(I(t,[f,y]),t instanceof f){let r=o()(t.value);const n=r.isNegative();if(n&&!e)throw EvalError("Unsigned Integer Converter expected nonnegative number but received: "+t);if(r.bitLength()+(e?1:0)>8*this.numBytes)throw EvalError("Cannot encode "+t.value+" in "+this.numBytes+" bytes.");n&&(r=r.not());const i=r.toArray(256).value;let u=new ArrayBuffer(this.numBytes),a=new Uint8Array(u);return a.set(i,this.numBytes-i.length),n&&a.forEach((t,e)=>a[e]=~t),this.bigEndian||a.reverse(),new y(u)}{const r=t.value.slice(0);let n=new Uint8Array(r);this.bigEndian||n.reverse();const i=e&&128&n[0];i&&n.forEach((t,e)=>n[e]=~t);const u=Array.from(n);let a=o.a.fromArray(u,256);return i&&(a=a.not()),new f(a)}}floatingPointCodec(t){throw EvalError("Not yet implemented")}}var X={},Y={};function tt(t,e){t=e.normalizePath(t);var r=X[t];if(r)return r;const n=V(e.load(t));if(1!==n.length)throw SyntaxError("A module file should contain exactly one object but received: "+n.length);const o=new l([],[],e);return r=new x(n[0],o,null),X[t]=r,r}function et(t,e){const r="No module found under literal sequence "+t.map(z).join(" ");if(t[0].eq(5)){var n=Y[5];for(const e of t.slice(1)){if(!(n instanceof g))throw EvalError(r);n=n.value[e.toString()]}return n}const o=function t(e,r,n){if(0===e.length)return n.isFile(r)?r:null;const o=e[0];const i=e.slice(1);const u=n.listdir(r);const a=u.map(e=>{if(!function(t,e){t=D(t);try{return R(t).eq(e)}catch(t){return!1}}(e,o))return null;const u=n.joinPath(r,e);return t(i,u,n)}).filter(t=>t);if(a.length>1)throw EvalError("Multiple files matched under "+dir);return a.length?a[0]:null}(t,".",e);if(!o)throw EvalError(r);return tt(o,e)}const rt=[function(t,e){return{"ㄱ":function(t){return C(t,1),I(t=t.map(e),[f,c]),P(t,c)?new c(t.every(q)):new f(t.map(q).reduce((function(t,e){return P([t,e],o.a)?t.times(e):t*e}),o.a.one))},"ㄷ":function(t){if(C(t,1),I(t=t.map(e),[f,c,h,v,y,g]),P(t,c))return new c(t.some(q));if(P(t,v))return new v(t.map(q).join(""));if(P(t,y)){const e=(t=t.map(q)).map(t=>t.byteLength).reduce((t,e)=>t+e,0),r=new ArrayBuffer(e),n=new Uint8Array(r);return t.reduce((function(t,e){return n.set(new Uint8Array(e),t),t+e.byteLength}),0),new y(r)}if(P(t,h))return new h(t.map(q).reduce((function(t,e){return t.concat(e)}),[]));if(P(t,g)){var r={};return t.forEach(t=>Object.assign(r,t.value)),new g(r)}return new f(t.map(q).reduce((function(t,e){return P([t,e],o.a)?t.plus(e):t+e}),o.a.zero))},"ㅅ":function(t){if(U(t,2),I(t=t.map(e),f),P(t,o.a))var r=t[0].value.pow(t[1].value);else r=Math.pow(t[0].value,t[1].value);return new f(r)}}},function(t,e){return{"ㅅㅈ":function(t){const r=t.length;if(r%2==1)throw SyntaxError("Dict requires even numbers of arguments but received: "+r);var n=t.filter((t,e)=>e%2==0),o=t.filter((t,e)=>e%2==1);n=(n=n.map(t=>A(t,e))).map(t=>L(t,e));var i={};for(let t=0;t<r/2;t++)i[n[t]]=o[t];return new g(i)},"ㅁㄹ":function(t){return new h(t)},"ㅁㅈ":function(t){if(U(t,[0,1]),0===t.length)return new v("");var r=e(t[0]);if(I(r,[f,v]),r instanceof v)return r;var n=r.value;return n===(0|n)&&(n|=0),new v(n.toString())},"ㅂㄱ":function(t){return U(t,0),new d}}},function(t,e){function r(e){return t(e,N)}return{"ㄴㄱ":function(t){return new $(t.map(r))},"ㅁㅂ":function(t){return U(t,1),new K(r(t[0]),e)},"ㅂㅂ":function(t){return U(t,1),new G(r(t[0]))}}},function(t,e){return{"ㄹ":function(t){return U(t,0),new m("ㄹ",t)},"ㅈㄹ":function(t){return U(t,1),I(t=t.map(e),v),new m("ㅈㄹ",t)},"ㄱㅅ":function(t){return U(t,1),new m("ㄱㅅ",t)},"ㄱㄹ":function(t){return C(t,1),new m("ㄱㄹ",t)}}},function(t,e){function r(t){if(0===t.length)return!0;if(!H(t.map(t=>t.length)))return!1;for(var e=t[0].length,r=0;r<e;r++)if(!n(t.map(t=>t[r])).value)return!1;return!0}function n(t){return P(t=t.map(e),M)?P(t,d)?new c(!0):P(t,f)?new c(0===(i=t.map(q)).length||i.slice(1).every((function(t){return i[0]instanceof o.a?i[0].eq(t):t instanceof o.a?t.eq(i[0]):i[0]==t}))):P(t,b)?new c(H(t)):P(t,h)?new c(r(t.map(q))):P(t,y)?new c(function(t){if(0===t.length)return!0;if(!H(t.map(t=>t.byteLength)))return!1;const e=t[0].byteLength,r=t.map(t=>new Uint8Array(t));for(let t=0;t<e;t++)if(!H(r.map(e=>e[t])))return!1;return!0}(t.map(q))):P(t,g)?new c(function(t){if(0===t.length)return!0;const e=t.map(t=>t.keys());return!!H(e.map(JSON.stringify))&&e[0].map(e=>t.map(t=>t.value[e])).map(n).every(q)}(t)):P(t,m)?H(t.map((function(t){return t.inst})))?new c(r(t.map((function(t){return t.argv})))):new c(!1):new c(H(t.map(q))):new c(!1);var i}return{"ㄴ":n,"ㅁ":function(t){return U(t,1),I(t=t.map(e),c),new c(!t[0].value)},"ㅈ":function(t){if(U(t,2),I(t=t.map(e),f),P(t,o.a))var r=t[0].value.lt(t[1].value);else r=t[0].value<t[1].value;return new c(r)},"ㅈㅈ":function(t){return U(t,0),new c(!0)},"ㄱㅈ":function(t){return U(t,0),new c(!1)}}},function(t,e){return Object.assign(Y,function(t,e){return{5:new g({5:new S((function(t){return U(t,[2,3]),t=t.map(e),new W(e,...t)}),"ㅂ ㅂ")})}}(0,e)),{"ㅂ":function(t){C(t,1);var r=t[0].env.utils;if(t.every(O))return et(t.map(t=>t.expr.value),r);U(t,1);var n=e(t[0]);return I(n,v),tt(n.value,r)}}},function(t,e){return{"ㅈㄷ":function(t){U(t,1),I(t=t.map(e),[h,v,y]);const r=t[0].value,n=P(t,y)?r.byteLength:r.length;return new f(o()(n))},"ㅂㅈ":function(t){U(t,[2,3,4]),I((t=t.map(e))[0],[h,v,y]),I(t.slice(1),f);var r=t[0].value,n=Math.round(t[1].value),o=t.length>2?Math.round(t[2].value):r.length;r=r.slice(n,o);var i=t.length>3?Math.round(t[3].value):1,u=(t,e)=>e%i==0;if(t[0]instanceof h)return new h(r.filter(u));if(t[0]instanceof v)return new v(r.split("").filter(u).join(""));if(t[0]instanceof y){const t=new Uint8Array(r).filter(u),e=new ArrayBuffer(t.byteLength);return new Uint8Array(e).set(t),new y(e)}},"ㅁㄷ":function(r){U(r,2);var n=e(r[0]);I(n,h);var o=t(r[1]);return new h(n.value.map(t=>o([t])))},"ㅅㅂ":function(r){U(r,2);var n=e(r[0]);I(n,h);var o=t(r[1]),i=(n=n.value).map(t=>o([t])).map(e);return I(i,c),i=i.map(q),new h(n.filter((t,e)=>i[e]))},"ㅅㄹ":function(r){U(r,[2,3]);var n=null;3===r.length&&(n=r[1],r=[r[0],r[2]]);var o=r;const i=(r=r.map(e))[0]instanceof h;function u(t){return i?t.slice().reverse():t}r=u(r),o=u(o);var a=t(o[0],[],r[0]);I(r[1],h);var s=u(r[1].value);return null===n&&(n=s[0],s=s.slice(1)),s.reduce((function(t,e){var r=u([t,e]);return a(r)}),n)}}},function(t,e){return{"ㅅㅅ":function(t){U(t,[1,2]);let r=(t=t.map(e))[0],n=t.length>1?t[1]:new f(10);I(r,v),I(n,f),r=r.value,n=n.value;try{return new f(o()(r,n))}catch(t){if(10==n&&!isNaN(+r))return new f(+r);const e=r.trim().split(".").concat([""]),o=e.join("");return function(t,e,r){const n="0123456789abcdefghijklmnopqrstuvwxyz".slice(0,r);if(-1===e.search("^[+-]?["+n+"]+$"))throw EvalError('Cannot convert "'+t+'" to Number.')}(r,o,n),new f(parseInt(o,n)/Math.pow(n,e[1].length))}},"ㅂㄹ":function(t){U(t,[1,2]),I(t=t.map(e),v);var r=t[0].value,n=t.length>1?t[1].value:"";return new h(r.split(n).map(t=>new v(t)))},"ㄱㅁ":function(t){U(t,[1,2]);var r=(t=t.map(e))[0],n=t.length>1?t[1]:new v("");I(r,h),I(n,v);var o=r.value.map(e);return I(o,v),new v(o.map(q).join(n.value))}}}].reduce((t,e)=>Object.assign(t,e(at,nt)),{});function nt(t){return t instanceof x?t.cache?t.cache:(t.cache=nt(ut(t.expr,t.env)),t.cache):t}function ot(t,e){return e>=0?t[e]:t[t.length+e]}function it(t,e){return e<0&&(e+=t.byteLength),t.slice(e,e+1)}function ut(t,e){if(t instanceof i)return new f(t.value);if(t instanceof u)return ot(e.funs,-t.rel-1);if(t instanceof a){if(e.funs.length!==e.args.length)throw EvalError("Assertion Error: Environment has "+e.funs.length+" funs and "+e.args.length+" args.");var r=ot(e.args,-t.relF-1),n=nt(ut(t.relA,e));if(I(n,f),(n=Math.round(n.value))<0||n>=r.length)throw EvalError("Out of Range: "+r.length+" args received but "+n+"-th argument requested");return r[n]}if(t instanceof s){var o=new l(e.funs.slice(),e.args,e.utils),c=new E(t.body,o);return o.funs.push(c),c}if(t instanceof p){var h=new x(t.fun,e,null),v=t.argv.map((function(t){return new x(t,e,null)}));return at(h,N)(v)}throw EvalError("Unexpected expression: "+t)}function at(t,e,r){if(O(t))return function(t){const e=z(t),r=rt[e];if(r)return r;throw EvalError("Unexpected builtin functions "+e)}(t.expr.value);if(t=r||nt(t),e=(e=e||[]).concat([b]),I(t,e),t instanceof b)return t.execute.bind(t);if(t instanceof c)return function(e){return U(e,2),e[t.value?0:1]};if(t instanceof g)return function(e){U(e,1);const r=A(e[0],nt),n=t.value[L(r,nt)];if(n)return n;throw EvalError("Key Error: dict "+t.value+" has no key "+r)};{const e=t instanceof y?it:ot;return function(r){U(r,1);const n=nt(r[0]);I(n,f);const o=Math.round(n.value);var i=e(t.value,o);const u=function(t,e){return e.find(e=>t instanceof e)}(t,[v,y]);return u&&(i=new u(i)),i}}}function st(t,e){I(t,m);var r=t.inst,n=t.argv;switch(r){case"ㄹ":return new v(e.input());case"ㅈㄹ":return e.print(n[0].value),new d;case"ㄱㅅ":return nt(n[0]);case"ㄱㄹ":var o=n.slice(),i=o.pop();I(o=o.map(nt),m),o=o.map(t=>pt(t,e));var u=nt(at(i)(o));return I(u,m),u}}function pt(t,e){for(I(t,m);t instanceof m;)t=st(t,e);return t}exports.main=function(t,e,r,n=!0){var o=V(t),i=new l([],[],r),u=o.map((function(t){return ut(t,i)}));return e.doIO=pt,u.map(t=>L(t,nt,e,n))}}]);