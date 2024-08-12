* Get the Viya Host URL if you deployed chronos here;
%let viyaHost=%sysfunc(getoption(SERVICESBASEURL)); 
* Specify the chronos endpoint;
%let chronosEndpoint = /forecast/predict/;

filename _ffmIn temp;

* Define the structure for the call;
data _null_;
	set sashelp.air(keep=air) end=EoF;

	file _ffmIn;

	if _n_ eq 1 then do;
		predictionLength = '{"prediction_length": ' || put(10, 8.) || ',';
		num_samples =  '"num_samples": ' || put(20, 8.) || ',';
		temperature = '"temperature": ' || put(1, 8.) || ',';
		top_k = '"top_k": ' || put(50, 8.) || ',';
		top_p = '"top_p": ' || put(1, 8.) || ',';
		dataBase = '"data": [';
		put predictionLength;
		put num_samples;
		put temperature;
		put top_k;
		put top_p;
		put dataBase;
	end;
            
	if not EoF then do;
		currentIteration = compress(put(air, 8.) || ',');
		put currentIteration;
	end;
	else if EoF then do;
		currentIteration = compress(put(air, 8.));
		dataClose = ']}';
		put currentIteration;
		put dataClose;
	end;
run;

filename _ffmOut temp;

* Call the chronos model;
proc http
	method = 'Post'
	url = "&viyaHost.&chronosEndpoint."
	in = _ffmIn
	out = _ffmOut;
	headers 'Content-Type' = 'application/json'
	'Accept' = 'text/csv';
quit;

* Import the returned CSV file;
proc import
	file = _ffmOut
	dbms = csv
	out = work.results
	replace;
run; quit;

* Clean up;
filename _ffmIn clear;
filename _ffmOut clear;
%symdel viyaHost chronosEndpoint;