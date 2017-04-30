function my_send(x){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "Music_Vibes.php"+x, true);
    xhttp.send();
}
function send_one(x){
    my_send("?Mode=One&Data="+x);
}
function send_term(){
    my_send("?Mode=Term");
}
function set_power(x){
    my_send("?Mode=Strength&Data="+x);
}
function send_init(x, y){
    my_send("?Mode=Init&Data="+x+y);
}
function send_push(x){
    my_send("?Mode=Push&Data="+x);
}
function send_lower(x){
    my_send("?Mode=Lower&Data="+x);
}
function send_clear(){
    my_send("?Mode=Clear");
}
