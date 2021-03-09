#pragma once
/*--------------------------------------------------------------------------+++
* Script Bookmark.
* 
* Describes the Bookmark struct.
*/

// visual studio
#include <string>

struct Bookmark {

    size_t iloc, sta, len, conn;
    std::string label, value;

    // empty constructor
    Bookmark():
        // init list
        iloc(0), sta(0), len(0), conn(0),
        label(), value() {
        // constructor body
        }

    // constructor for visible (in-text)
    Bookmark(
        size_t iloc, size_t sta, size_t len, size_t conn,
        std::string label ):
        // init list
        iloc(iloc), sta(sta), len(len), conn(conn),
        label(label), value() {
        // constructor body
        }

    // constructor for invisible (just value)
    Bookmark(
        size_t iloc, size_t conn,
        std::string label, std::string value ):
        // init list
        iloc(iloc), sta(0), len(0), conn(conn),
        label(label), value() {
        // constructor body
        }

    // destructor
    ~Bookmark() {
        // destructor body
        }

    }; // struct Bookmark...

//--------------------------------------------------------------------------+++
// конец 2021.03.02 → 2021.03.05
