void test(void){
    int g;
    g = 4;
    return;
}

void main(void){
    int a;
    //a = test();
    a = 1;
    switch (a){
        case 1: a = 2;
                switch (a){
                    case 3: a = 5;
                    case 5: a = 6;
                            break;
                    default: test();
                }
        case 2: a = 4;
                break;
        default: a = a * 4;
    }
}
