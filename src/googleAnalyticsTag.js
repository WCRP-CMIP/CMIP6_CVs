function loadGoogleAnalytics(){
    var ga = document.createElement('script');
    ga.type = 'text/javascript';
    ga.async = true;
    ga.src = 'https://www.googletagmanager.com/gtag/js?id=UA-3843414-4';

    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(ga, s);
}

loadGoogleAnalytics(); //Create the script

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'UA-3843414-4');

/*
https://stackoverflow.com/questions/1131079/is-it-possible-to-put-google-analytics-code-in-an-external-js-file
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-3843414-4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-3843414-4');
</script>
*/