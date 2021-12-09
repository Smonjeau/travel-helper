const API_URL = 'http://localhost:8000/queries';

const resultsModal = UIkit.modal('#resultsModal');
const resultsModalContent = $('#resultsModal .uk-modal-body');


function showFlights(response) {
    resultsModal.show();
    resultsModalContent.html('');
    let aux = "";
    response.forEach(tracks => {
        aux = "<div class=\"uk-card uk-card-default uk-card-body uk-margin-top uk-margin-bottom\">";
        tracks.forEach(track => {
            aux += "<div uk-grid><div class=\"uk-width-1-2 uk-text-center\"><p><b>" + track.source + " → " + track.destination;
            aux += "</b></p><div uk-grid><div class=\"uk-width-1-2 uk-text-muted uk-text-small\">"+track.source_city+",<br>"+track.source_country
            aux += "</div><div class=\"uk-width-1-2 uk-text-muted uk-text-small\">"+track.destination_city+",<br>"+track.destination_country
            aux += "</div></div></div><div class=\"uk-width-1-2 uk-text-center\"><p>" + track.airline_name + "<br>" + Math.ceil(track.distance) + " km</p>";
            aux += "</div></div>";
        });                
        aux += "</div>";
        resultsModalContent.append(aux)
    });
}


function showAirports(response, key) {
    resultsModal.show();
    resultsModalContent.html('');
    let aux = "";
    response.forEach(airport => {
        aux = "<div class=\"uk-card uk-card-default uk-card-body uk-margin-top uk-margin-bottom\">";

        aux += "<div uk-grid><div class=\"uk-width-1-4 uk-text-center\"><b>"+(key == 'incoming' ? airport.incoming : airport.outgoing)+"</b></div>";
        aux += "<div class=\"uk-width-1-4 uk-text-center\">" + airport.iata + " / " + airport.icao;
        aux += "</div><div class=\"uk-width-1-4 uk-text-center\">"+airport.name
        aux += "</div><div class=\"uk-width-1-4 uk-text-center\">" + airport.city + ", " + airport.country;
        aux += "</div></div></div>";
        
        resultsModalContent.append(aux)
    });
}

$('#search1').click(function(){
    let source = $('#source1').val();
    let destination = $('#destination1').val();
    let code = $('#code1').val();
    let page = $('#page1').val();

    if(code.toLowerCase() === 'iata'){
        if(source.length != 3 || destination.length != 3) {
            alert("Worng parameters")
            return
        }
    } else if(code.toLowerCase() === 'icao'){
        if(source.length != 4 || destination.length != 4) {
            alert("Worng parameters")
            return
        }
    } else {
        alert("Worng parameters")
        return
    }

    $.ajax({
        url: API_URL + '/all_routes',
        type: "GET",
        crossDomain: true,
        data: { 
            source_airport_code: source,
            destination_airport_code: destination,
            airport_code_type: code,
            page: parseInt(page)
        },
        dataType: "json",
        success: function (response) {
            showFlights(response)
        },
        error: function (xhr, status) {
            alert("error");
        }
    });
})


$('#search2').click(function(){
    let source = $('#source2').val();
    let destination = $('#destination2').val();
    let scales = $('#scales2').val();
    let code = $('#code2').val();
    let page = $('#page2').val();

    if(code.toLowerCase() === 'iata'){
        if(source.length != 3 || destination.length != 3) {
            alert("Worng parameters")
            return
        }
    } else if(code.toLowerCase() === 'icao'){
        if(source.length != 4 || destination.length != 4) {
            alert("Worng parameters")
            return
        }
    } else {
        alert("Worng parameters")
        return
    }

    $.ajax({
        url: API_URL + '/all_routes_with_scales',
        type: "GET",
        crossDomain: true,
        data: { 
            source_airport_code: source,
            destination_airport_code: destination,
            airport_code_type: code,
            scales: scales,
            page: parseInt(page)
        },
        dataType: "json",
        success: function (response) {
            showFlights(response)
        },
        error: function (xhr, status) {
            alert("error");
        }
    });

})

$('#search3').click(function(){
    let source = $('#source3').val();
    let scales = $('#scales3').val();
    let code = $('#code3').val();
    let page = $('#page3').val();

    if(code.toLowerCase() === 'iata'){
        if(source.length != 3) {
            alert("Worng parameters")
            return
        }
    } else if(code.toLowerCase() === 'icao'){
        if(source.length != 4) {
            alert("Worng parameters")
            return
        }
    } else {
        alert("Worng parameters")
        return
    }

    $.ajax({
        url: API_URL + '/airports_reachable_from_airport',
        type: "GET",
        crossDomain: true,
        data: { 
            source_airport_code: source,
            airport_code_type: code,
            scales: scales,
            page: parseInt(page)
        },
        dataType: "json",
        success: function (response) {
            showFlights(response)
        },
        error: function (xhr, status) {
            alert("error");
        }
    });

})

$('#search4').click(function(){
    let source = $('#source4').val();
    let destination = $('#destination4').val();
    let code = $('#code4').val();

    if(code.toLowerCase() === 'iata'){
        if(source.length != 3 || destination.length != 3) {
            alert("Worng parameters")
            return
        }
    } else if(code.toLowerCase() === 'icao'){
        if(source.length != 4 || destination.length != 4) {
            alert("Worng parameters")
            return
        }
    } else {
        alert("Worng parameters")
        return
    }

    $.ajax({
        url: API_URL + '/shortest_route_in_scales',
        type: "GET",
        crossDomain: true,
        data: { 
            source_airport_code: source,
            destination_airport_code: destination,
            airport_code_type: code
        },
        dataType: "json",
        success: function (response) {
            showFlights(response)
        },
        error: function (xhr, status) {
            alert("error");
        }
    });

})

$('#search5').click(function(){
    let source = $('#source5').val();
    let destination = $('#destination5').val();
    let avoidairline = $('#avoidairline5').val();
    let code = $('#code5').val();
    let page = $('#page5').val();

    if(code.toLowerCase() === 'iata'){
        if(source.length != 3 || destination.length != 3) {
            alert("Worng parameters")
            return
        }
    } else if(code.toLowerCase() === 'icao'){
        if(source.length != 4 || destination.length != 4) {
            alert("Worng parameters")
            return
        }
    } else {
        alert("Worng parameters")
        return
    }

    $.ajax({
        url: API_URL + '/all_routes_avoiding_airline',
        type: "GET",
        crossDomain: true,
        data: { 
            source_airport_code: source,
            destination_airport_code: destination,
            airport_code_type: code,
            airline_code: avoidairline,
            page: parseInt(page)
        },
        dataType: "json",
        success: function (response) {
            showFlights(response)
        },
        error: function (xhr, status) {
            alert("error");
        }
    });

})



$('#search6').click(function(){
    let source = $('#source6').val();
    let destination = $('#destination6').val();
    let avoidairport = $('#avoidairport6').val();
    let code = $('#code6').val();
    let page = $('#page6').val();

    if(code.toLowerCase() === 'iata'){
        if(source.length != 3 || destination.length != 3) {
            alert("Worng parameters")
            return
        }
    } else if(code.toLowerCase() === 'icao'){
        if(source.length != 4 || destination.length != 4) {
            alert("Worng parameters")
            return
        }
    } else {
        alert("Worng parameters")
        return
    }

    $.ajax({
        url: API_URL + '/all_routes_avoiding_airport',
        type: "GET",
        crossDomain: true,
        data: { 
            source_airport_code: source,
            destination_airport_code: destination,
            airport_code_type: code,
            airport_code: avoidairport,
            page: parseInt(page)
        },
        dataType: "json",
        success: function (response) {
            showFlights(response)
        },
        error: function (xhr, status) {
            alert("error");
        }
    });

})



$('#search7').click(function(){
    let number = $('#number7').val();


    $.ajax({
        url: API_URL + '/most_popular_airports',
        type: "GET",
        crossDomain: true,
        data: { 
            number_of_airports: number
        },
        dataType: "json",
        success: function (response) {
            showAirports(response, "incoming")
        },
        error: function (xhr, status) {
            alert("error");
        }
    });

})


$('#search8').click(function(){
    let number = $('#number8').val();


    $.ajax({
        url: API_URL + '/airports_with_most_routes',
        type: "GET",
        crossDomain: true,
        data: { 
            number_of_airports: number
        },
        dataType: "json",
        success: function (response) {
            showAirports(response, "outgoing")
        },
        error: function (xhr, status) {
            alert("error");
        }
    });

})