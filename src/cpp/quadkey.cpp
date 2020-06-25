/*
    cf. https://cttr.jp/2019/04/10/post-453/
*/
#include <math.h>
#include <unistd.h>
#include <string>
#include <iostream>
#include <sstream>

std::string latlon_to_quadkey(double lat, double lon, int zoom_level) {
    // (lat, lon) to tile(x, y)
    double x = (lon / 180 + 1) * std::pow(2, zoom_level) / 2;
    int xtile = int(x);
    double y = ((-log(tan((45 + lat / 2) * M_PI / 180)) + M_PI) * std::pow(2, zoom_level) / (2 * M_PI));
	int ytile = int(y);

    // tile(x, y) to quadkey
    std::string quadKey;
    for (int i = zoom_level; i > 0; i--) {
        int digit = 0;
        int mask = 1 << (i-1);
        if ((xtile & mask) != 0) {
            digit++;
        }
        if ((ytile & mask) != 0) {
            digit++;
            digit++;
        }
        quadKey += std::to_string(digit);
    }
    return quadKey;
}

int main(int argc, char* argv[]) {
    int zoom_level = 20;

    int opt;
    while ((opt = getopt(argc, argv, "z:")) != -1) {
        switch (opt) {
        case 'z':
            zoom_level = std::stoi(optarg);
            break;
        }
    }

    std::string l;
    while(std::getline(std::cin, l)) {
        auto ss = std::stringstream(l);
        double lat, lon;
        ss >> lat >> lon;

        std::string quadkey = latlon_to_quadkey(lat, lon, zoom_level);
        std::cout << quadkey << std::endl;
    }
}
