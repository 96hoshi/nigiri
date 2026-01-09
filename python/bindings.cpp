#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>

#include "nigiri/timetable.h"
#include "nigiri/routing/query.h"
#include "nigiri/routing/journey.h"
#include "nigiri/routing/raptor_search.h"
#include "nigiri/routing/search.h"
#include "nigiri/loader/gtfs/load_timetable.h"
#include "nigiri/loader/dir.h"
#include "nigiri/types.h"

namespace py = pybind11;
using namespace nigiri;
using namespace nigiri::routing;

PYBIND11_MODULE(_nigiri, m) {
    m.doc() = "Nigiri transit routing library Python bindings";

    // Direction enum
    py::enum_<direction>(m, "Direction")
        .value("FORWARD", direction::kForward)
        .value("BACKWARD", direction::kBackward)
        .export_values();

    // Location match mode
    py::enum_<location_match_mode>(m, "LocationMatchMode")
        .value("EXACT", location_match_mode::kExact)
        .value("EQUIVALENT", location_match_mode::kEquivalent)
        .value("ONLY_CHILDREN", location_match_mode::kOnlyChildren)
        .value("INTERMODAL", location_match_mode::kIntermodal)
        .export_values();

    // Offset for start/destination
    py::class_<offset>(m, "Offset")
        .def(py::init<location_idx_t, duration_t, transport_mode_id_t>(),
             py::arg("location"), py::arg("duration"), py::arg("transport_mode_id") = 0)
        .def_property_readonly("target", &offset::target)
        .def_property_readonly("duration", [](offset const& o) { 
            return o.duration().count(); 
        })
        .def("__repr__", [](offset const& o) {
            return "<Offset to " + std::to_string(to_idx(o.target())) + 
                   " in " + std::to_string(o.duration().count()) + " min>";
        });

    // Routing query
    py::class_<query>(m, "Query")
        .def(py::init<>())
        .def_readwrite("use_start_footpaths", &query::use_start_footpaths_)
        .def_readwrite("max_transfers", &query::max_transfers_)
        .def_readwrite("min_connection_count", &query::min_connection_count_)
        .def("add_start", [](query& q, location_idx_t loc, int duration_min) {
            q.start_.emplace_back(loc, duration_t{duration_min}, 0);
        }, py::arg("location"), py::arg("duration_minutes") = 0)
        .def("add_destination", [](query& q, location_idx_t loc, int duration_min) {
            q.destination_.emplace_back(loc, duration_t{duration_min}, 0);
        }, py::arg("location"), py::arg("duration_minutes") = 0)
        .def("set_start_time", [](query& q, int64_t unix_seconds) {
            auto const minutes = unix_seconds / 60;
            q.start_time_ = unixtime_t{std::chrono::minutes{minutes}};
        }, py::arg("unix_seconds"))
        .def("__repr__", [](query const& q) {
            return "<Query: " + std::to_string(q.start_.size()) + 
                   " start(s) → " + std::to_string(q.destination_.size()) + " dest(s)>";
        });

    // Journey leg
    py::class_<journey::leg>(m, "JourneyLeg")
        .def_property_readonly("from_location", [](journey::leg const& l) { 
            return to_idx(l.from_); 
        })
        .def_property_readonly("to_location", [](journey::leg const& l) { 
            return to_idx(l.to_); 
        })
        .def_property_readonly("departure_time", [](journey::leg const& l) {
            return l.dep_time_.time_since_epoch().count();
        })
        .def_property_readonly("arrival_time", [](journey::leg const& l) {
            return l.arr_time_.time_since_epoch().count();
        })
        .def_property_readonly("is_transport", [](journey::leg const& l) {
            return std::holds_alternative<journey::run_enter_exit>(l.uses_);
        })
        .def_property_readonly("is_footpath", [](journey::leg const& l) {
            return std::holds_alternative<footpath>(l.uses_);
        })
        .def("__repr__", [](journey::leg const& l) {
            std::string type = std::holds_alternative<journey::run_enter_exit>(l.uses_) ? "Transport" :
                              std::holds_alternative<footpath>(l.uses_) ? "Walk" : "Offset";
            return "<" + type + ": " + std::to_string(to_idx(l.from_)) + 
                   " → " + std::to_string(to_idx(l.to_)) + ">";
        });

    // Journey
    py::class_<journey>(m, "Journey")
        .def_readonly("legs", &journey::legs_)
        .def_property_readonly("start_time", [](journey const& j) {
            return j.start_time_.time_since_epoch().count();
        })
        .def_property_readonly("dest_time", [](journey const& j) {
            return j.dest_time_.time_since_epoch().count();
        })
        .def_property_readonly("destination", [](journey const& j) { 
            return to_idx(j.dest_); 
        })
        .def_property_readonly("transfers", [](journey const& j) { 
            return j.transfers_; 
        })
        .def_property_readonly("travel_time_minutes", [](journey const& j) {
            return j.travel_time().count();
        })
        .def("__repr__", [](journey const& j) {
            return "<Journey: " + std::to_string(j.legs_.size()) + 
                   " legs, " + std::to_string(j.transfers_) + " transfers, " +
                   std::to_string(j.travel_time().count()) + " min>";
        });

    // Timetable
    py::class_<timetable>(m, "Timetable")
        .def(py::init<>())
        .def("n_locations", &timetable::n_locations)
        .def("get_location_name", [](timetable const& tt, location_idx_t loc) {
            return std::string(tt.get_default_name(loc));
        }, py::arg("location_idx"))
        .def("get_location_coords", [](timetable const& tt, location_idx_t loc) {
            auto const& coords = tt.locations_.coordinates_[loc];
            return py::make_tuple(coords.lat_, coords.lng_);
        }, py::arg("location_idx"))
        .def("find_location", [](timetable const& tt, std::string const& id, uint16_t src_num) -> py::object {
            source_idx_t const src{src_num};
            location_id const loc_id{id, src};
            auto const it = tt.locations_.location_id_to_idx_.find(loc_id);
            if (it == tt.locations_.location_id_to_idx_.end()) {
                return py::none();
            }
            return py::cast(it->second);
        }, py::arg("id"), py::arg("source") = 0)
        .def("route", [](timetable const& tt, query q, direction dir) -> std::vector<journey> {
            search_state s_state;
            raptor_state r_state;
            auto result = raptor_search(tt, nullptr, s_state, r_state, std::move(q), dir);
            if (result.journeys_ == nullptr) {
                return {};
            }
            return std::vector<journey>(result.journeys_->begin(), result.journeys_->end());
        }, py::arg("query"), py::arg("direction") = direction::kForward,
           "Perform routing and return list of journeys")
        .def("__repr__", [](timetable const& tt) {
            return "<Timetable with " + std::to_string(tt.n_locations()) + " locations>";
        });

    // GTFS loader
    m.def("load_timetable", [](std::string const& gtfs_path) {
        timetable tt;
        nigiri::loader::loader_config const cfg{
            .link_stop_distance_ = 100U,
            .default_tz_ = "",
            .bikes_allowed_default_ = {},
            .cars_allowed_default_ = {},
            .extend_calendar_ = false,
            .user_script_ = "",
            .base_paths_ = {}
        };
        source_idx_t src{0};
        nigiri::loader::gtfs::load_timetable(cfg, src, nigiri::loader::fs_dir{gtfs_path}, tt);
        return tt;
    }, py::arg("gtfs_path"), "Load GTFS data into a timetable");
    
    m.def("hello", []() { return "Nigiri Python bindings loaded successfully!"; });
}
