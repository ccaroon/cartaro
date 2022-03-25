from cartaro.model.time_off.holiday import Holiday
import cartaro.controller.base as base

holidays = base.create_controller("holidays", Holiday)
