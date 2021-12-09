const API_URL = 'http://localhost:8000/queries';

const resultsModal = UIkit.modal('#resultsModal');
const resultsModalContent = $('#resultsModal .uk-modal-body');

//TODO Los airline_id cambiar por nombre de la aerolinea

$('#search1').click(function(){
    let source = $('#source1').val();
    let destination = $('#destination1').val();
    let code = $('#code1').val();

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
            airport_code_type: code
        },
        dataType: "json",
        success: function (response) {
            resultsModal.show();
            resultsModalContent.html('');
            let aux = "";
            response.forEach(tracks => {
                aux = "<div class=\"uk-card uk-card-default uk-card-body uk-margin-top uk-margin-bottom\">";
                tracks.forEach(track => {
                    aux += "<p>" + track.source + " -> " + track.destination + " | " + track.airline_id + " " + Math.ceil(track.distance) + "km</p>";
                });
                aux += "</div>";
                resultsModalContent.append(aux)
            });
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
            scales: scales
        },
        dataType: "json",
        success: function (response) {
            resultsModal.show();
            resultsModalContent.html('');
            let aux = "";
            response.forEach(tracks => {
                aux = "<div class=\"uk-card uk-card-default uk-card-body uk-margin-top uk-margin-bottom\">";
                tracks.forEach(track => {
                    aux += "<p>" + track.source + " -> " + track.destination + " | " + track.airline_id + " " + Math.ceil(track.distance) + "km</p>";
                });
                aux += "</div>";
                resultsModalContent.append(aux)
            });
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
            scales: scales
        },
        dataType: "json",
        success: function (response) {
            resultsModal.show();
            resultsModalContent.html('');
            let aux = "";
            response.forEach(tracks => {
                aux = "<div class=\"uk-card uk-card-default uk-card-body uk-margin-top uk-margin-bottom\">";
                tracks.forEach(track => {
                    aux += "<p>" + track.source + " -> " + track.destination + " | " + track.airline_id + " " + Math.ceil(track.distance) + "km</p>";
                });
                aux += "</div>";
                resultsModalContent.append(aux)
            });
        },
        error: function (xhr, status) {
            alert("error");
        }
    });

})