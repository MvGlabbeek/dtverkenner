document$.subscribe(function () {
  var t = document.getElementById("register");
  if (t && !t.dataset.dt) {
    t.dataset.dt = "1";
    new DataTable(t, {
      pageLength: 25, scrollX: true,
      language: { url: "https://cdn.datatables.net/plug-ins/2.1.8/i18n/nl-NL.json" }
    });
  }
});
