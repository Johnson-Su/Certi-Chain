class HashGetter{
  url;
  hashCode;
  transactionNumber;

  constructor(url) {
    this.url = url;
    this.hashCode = "";
    this.splitUrl();
  }

  splitHashAndTransaction() {
    this.transactionNumber = this.hashCode.substring(this.hashCode.indexOf("t="));
    this.hashCode = this.hashCode.substring(this.hashCode.indexOf("h="), this.hashCode.indexOf("t="));
  }
  
  splitUrl() {
    let hashCode = "";
    let past_h = false;
    for (var i = 0; i < this.url.length; i++) {
      if (this.url[i+2] == "=" && this.url[i+1] == "h") {
        past_h = true;
      }
      if (past_h == true) {
        this.hashCode += this.url[i];
      }
    }
    this.transactionNumber = this.hashCode.substring(this.hashCode.indexOf("t=") + 2);
    this.hashCode = this.hashCode.substring(this.hashCode.indexOf("h=") + 2, 
    this.hashCode.indexOf("t="));
  }

    
  getHashCode(){
    document.getElementById("hashCode").innerHTML = "The hash code is: " + this.hashCode;
    document.getElementById("transactionCode").innerHTML = "The transaction number is: " + this.transactionNumber;
  }
}