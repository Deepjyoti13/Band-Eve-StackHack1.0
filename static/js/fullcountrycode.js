var input = document.querySelector('#phone');
var countrydata = window.intlTelInputGlobals.getCountryData();
var addressdropdown = document.querySelector('#address-country');
var iti = window.intlTelInput(input, {
  utilsScript: "{% static '/js/utils.js' %}"
});
for (var i = 0; i < countrydata.length; i++)
{
  var country = countrydata[i];
  var optionnode = document.createElement("option");
  optionnode.value = country.iso2;
  var textnode = document.createTextNode(country.name);
  optionnode.appendChild(textnode);
  addressdropdown.appendChild(optionnode);
}
addressdropdown.value = iti.getSelectedCountryData.iso2;
input.addEventListener('countrychange', function () {
  addressdropdown.value = iti.getSelectedCountryData().iso2;
});
addressdropdown.addEventListener('change', function () {
  iti.setCountry(this.value)
});
