int b;
void main(void) {
	int c;
	int foo(int a) {
		a = a * -2;
	}
	int foo2(void) {
		c = c + 1;
	}
	b = foo2();
	if (b < 0) {
		c = foo(-3 + b);
		break;
	} else c = foo(2 * b + 1);
}