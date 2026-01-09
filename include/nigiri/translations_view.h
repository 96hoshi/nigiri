#pragma once

#include <vector>
#include <string_view>

#include "nigiri/timetable.h"

namespace nigiri {

// Disabled: std::views::zip not available in GCC 12
// Workaround: return empty vector, not actually used
inline auto get_translation_view(timetable const& tt,
                                 translation_idx_t const t) {
  return std::vector<std::pair<language_idx_t, std::string_view>>{};
}

}  // namespace nigiri