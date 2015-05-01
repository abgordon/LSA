var unirest = require('unirest');
var fs = require('fs');
var readline = require('readline');
var LineByLineReader = require('line-by-line'),
    lr = new LineByLineReader('requests.txt');



//Asynchronous requests to wikipedia API to collect raw text of articles
//These are from the "Central Articles" page of wikipedia, countries/nations omitted
//This can be used to demonstrate the vector application, or you can use your own texts
lr.on('line', function (line) {

    var title = line
          console.log("Currently requesting "+ title)

          var init = unirest.get("https://community-wikipedia.p.mashape.com/api.php?action=query&format=json&prop=revisions&rvprop=content&titles="+title)
            .header("X-Mashape-Key", "coUtA6xOROmshQHp8rFDi5ddoI0vp1w3GTBjsnfJsZiuoAHXkv")
            .header("Accept", "application/json")
            .end(function (result) {

              console.log("currently requesting " + title)

              for (var key in result.body.query.pages){


                var attrName = key

                var attrValue = result.body.query.pages[key]
                if (attrValue.revisions == undefined){
                    console.log("couldn't find "+ title)
                 }
                 else{
                    var text = attrValue.revisions[0]['*']
                    var titlestring = title + ".txt"
                    var path = "./articleJSON/" +titlestring
                           
                    console.log("Appending to "+ path)
                    fs.writeFile(path, text);
                    fs.appendFile(path, "\n")
                    console.log("successfully wrote to file")
                   }
                
                 }
            //end unirest
            });

});

