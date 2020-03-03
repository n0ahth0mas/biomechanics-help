//Select Elements
//Text Sections by Letter
const glossA = document.getElementById("glossA")
const glossB = document.getElementById("glossB")
const glossC = document.getElementById("glossC")
const glossD = document.getElementById("glossD")
const glossE = document.getElementById("glossE")
const glossF = document.getElementById("glossF")
const glossG = document.getElementById("glossG")
const glossH = document.getElementById("glossH")
const glossI = document.getElementById("glossI")
const glossJ = document.getElementById("glossJ")
const glossK = document.getElementById("glossK")
const glossL = document.getElementById("glossL")
const glossM = document.getElementById("glossM")
const glossN = document.getElementById("glossN")
const glossO = document.getElementById("glossO")
const glossP = document.getElementById("glossP")
const glossQ = document.getElementById("glossQ")
const glossR = document.getElementById("glossR")
const glossS = document.getElementById("glossS")
const glossT = document.getElementById("glossT")
const glossU = document.getElementById("glossU")
const glossV = document.getElementById("glossV")
const glossW = document.getElementById("glossW")
const glossX = document.getElementById("glossX")
const glossY = document.getElementById("glossY")
const glossZ = document.getElementById("glossZ")

//var sections = [glossA,glossB,glossC,glossD,glossE,glossF,glossG,glossH,glossI,glossJ,glossK,glossL,glossM,glossN,glossO,glossP,glossQ,glossR,glossS,glossT,glossU,glossV,glossW,glossX,glossY,glossZ];
var terms = {{terms}};
var defns = {{defns}};

var alpha = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];

console.log(js_terms)
//cant use docu write, try innerhtml with directs to id tags in html
function renderGlossary(){
    document.write("Hello World");
    glossA.innerhtml = "<p>Fuckity Fuck!</p>";
    for(i=0; i < alpha.length; i++){
        document.write(alpha[i]);
        for(j=0; j < terms.length; j++){
            if(terms[j].charAt(0)==alpha[i]){
                //document.write(terms[j] + ": " + defns[j] + "\n");
            }
        }
    }
}