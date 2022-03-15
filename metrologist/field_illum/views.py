"""
homogeneity report elements to include inside 
templates/homogeneities/homogeneity.html
"""
from flask import Blueprint, render_template
from metrologist.field_illum.models import Homogeneity

@blueprint.route("/")
def homogeneity():
    """ return all elements of homogeneity report inside homogeneity.html """

    # max_region_table
    
    max_region_table = select(
        homogeneities.c.max_region_table_nb_pixels,
        homogeneities.c.max_region_table_center_of_mass,
        homogeneities.c.max_region_table_max_intensity
    )

    max_region_table.columns = [
        "nb_pixels",
        "center of mass",
        "max_intensity"
    ]

    # intensity_plot
    intensity_plot_data = select(
        homogeneities.c.intensity_plot_data_x_axis_V_seg,
        homogeneities.c.intensity_plot_data_y_axis_V_seg,
        homogeneities.c.intensity_plot_data_x_axis_H_seg,
        homogeneities.c.intensity_plot_data_y_axis_H_seg,
        homogeneities.c.intensity_plot_data_x_axis_diagUD,
        homogeneities.c.intensity_plot_data_y_axis_diagUD,
        homogeneities.c.intensity_plot_data_x_axis_diagDU,
        homogeneities.c.intensity_plot_data_y_axis_diagDU
    )

    def get_intensity_plot_(data=intensity_plot_data):
        x_data = data.iloc[:, [0,2,4,6]]
        y_data = data.iloc[:, [1,3,5,7]]

        # plot
        colors = ["b", "g", "r", "y"]
        labels = ["V_seg", "H_seg", "diagUD", "diagDU"]

        fig = plt.figure()
        for i in range(8):
            x_values = x_data.iloc[:,i]
            y_values = y_data.iloc[:,i]
            plt.plot(x_values, y_values, color=colors[i], label=labels[i], figure=fig)        
        
        plt.axvline(0, linestyle='--')
        plt.title("Intensity Profiles", figure=fig)
        plt.xlim((min(get_x_axis(diagUD))-25, max(get_x_axis(diagUD))+25))
        plt.legend()
 
    # profile_stat_table 
    profile_state_table = select(
        homogeneities.c.profile_stat_table_location,
        homogeneities.c.profile_stat_table_intensity,
        homogeneities.c.profile_stat_table_intensity_relative_to_max
    )

    profile_state_table.columns = [
        "location",
        "intensity",
        "relative_to_max"
    ]

    # norm_intensity_profile
    norm_intensity_data = db.select(homogeneities.c.intensity_plot_data)
    def get_norm_intensity_profile_(norm_intensity_data=norm_intensity_data):
        return homo.get_norm_intensity_profile(norm_intensity_data)

    return render_template(
        "homogeneity.html",
        max_region_table=max_region_table,
        intensity_plot=get_intensity_plot_(),
        profile_state_table=profile_state_table,
        norm_intensity_profile=get_norm_intensity_profile_()
        )
