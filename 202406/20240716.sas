data mydata_char;
    set mydata;
    char_variable = put(numeric_variable, 16.);
run;