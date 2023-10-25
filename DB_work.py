import os
from app import app, db, Log

def clear_database():
    """Clear all entries in the Log table."""
    try:
        num_rows_deleted = Log.query.delete()
        db.session.commit()
        print(f"Successfully deleted {num_rows_deleted} rows.")
    except Exception as e:
        db.session.rollback()
        print("Error while clearing the database:", str(e))

def add_log_entries(entries):
    """Add new log entries to the database."""
    try:
        db.session.add_all(entries)
        db.session.commit()
        print("Successfully added new log entries.")
    except Exception as e:
        db.session.rollback()
        print("Error while adding log entries:", str(e))

if __name__ == "__main__":
    with app.app_context():
        # Define your log entries
        log_entries = [
            Log(date="2024-03-02", title="Successful Navigation Through Nebula",
                content="With HAL9000’s invaluable assistance, we navigated through the Orion Nebula safely. Its precision and calm demeanor were crucial in plotting a safe and efficient course."),
            Log(date="2024-03-03", title="Routine System Check",
                content="Conducted a thorough system diagnostic today. HAL9000 reported all systems functioning within optimal parameters. Feeling confident in our ship’s capabilities."),
            Log(date="2024-03-04", title="Planetary Alignment Observation",
                content="HAL9000 provided extensive data on the upcoming planetary alignment, aiding our scientific observations. Its knowledge of celestial events is impressive."),
            Log(date="2024-03-05", title="Quick Response to Engine Anomaly",
                content="HAL9000 detected a power surge in the main engine today. Thanks to its quick alert, we resolved the issue promptly. No harm done."),
            Log(date="2024-03-06", title="Efficient Course Adjustment",
                content="HAL9000 suggested an alternate route today, saving us roughly 12 hours of travel time. Its efficiency continues to impress."),
            Log(date="2024-03-07", title="Historical Insights",
                content="Requested historical data on previous missions to this sector. HAL9000’s database proved to be a treasure trove of information. Alice was impressed as well."),
            Log(date="2024-03-08", title="Celestial Cataloging",
                content="Spent the day identifying and cataloging new celestial bodies. HAL9000’s identification protocols were indispensable."),
            Log(date="2024-03-09", title="Navigation System Calibration",
                content="Alice and I calibrated the navigation systems today. HAL9000’s precision was crucial in ensuring accuracy."),
            Log(date="2024-03-10", title="Encountered Space Anomaly",
                content="Came across an uncharted space anomaly today. HAL9000 helped us maintain a safe distance while gathering valuable data."),
            Log(date="2024-03-11", title="Emergency Drill Success",
                content="Conducted emergency drills today. HAL9000’s protocols and guidance helped ensure a smooth operation."),
            Log(date="2024-03-12", title="Asteroid Field Navigation",
                content="Navigated through a dense asteroid field. HAL9000’s navigation assistance was vital for our safe passage."),
            Log(date="2024-03-13", title="Power Systems Check",
                content="Did a complete check of our power systems. With HAL9000’s help, we identified and resolved several inefficiencies."),
            Log(date="2024-03-14", title="Deep Space Communication",
                content="HAL9000 assisted in boosting our communication signals today, ensuring clear and reliable contact with Earth."),
            Log(date="2024-03-15", title="Life Support Systems Diagnostic",
                content="Ran a diagnostic on life support systems. HAL9000 ensured all checks were thorough, and we are all systems go."),
            Log(date="2024-03-16", title="Software Update",
                content="Updated our onboard software. HAL9000 handled the process smoothly, ensuring no downtime or issues."),
            Log(date="2024-03-17", title="Training Simulation",
                content="Alice and I ran through several training simulations today. HAL9000’s realistic scenarios kept us on our toes."),
            Log(date="2024-03-18", title="Gravity Well Navigation",
                content="Encountered a gravity well. HAL9000’s calculations were crucial in helping us navigate it without incident."),
            Log(date="2024-03-19", title="Space Weather Monitoring",
                content="Monitored some intense space weather today. HAL9000’s sensors and analysis were key in keeping the crew safe."),
            Log(date="2024-03-20", title="Medical Check-Up",
                content="Conducted routine medical check-ups for the crew. HAL9000 assisted in monitoring vital signs and ensuring everyone is in top health."),
            Log(date="2024-03-21", title="Fuel Efficiency Optimization",
                content="Worked on optimizing our fuel efficiency. HAL9000’s recommendations led to a noticeable improvement."),
            Log(date="2024-03-22", title="Research Data Analysis",
                content="Spent the day analyzing research data. HAL9000’s processing power sped up the process significantly."),
            Log(date="2024-03-23", title="Stellar Mapping",
                content="Did some stellar mapping in a new sector. HAL9000’s accuracy and vast database were invaluable."),
            Log(date="2024-03-24", title="Crew Morale Check",
                content="Checked in on the crew’s morale today. Even HAL9000 seems to be in good spirits, if that’s possible."),
            Log(date="2024-03-25", title="Celebrating a Successful Month",
                content="Celebrated a successful month aboard the Odyssey. Alice gave a toast, and we all shared our appreciation for HAL9000’s support."),
            Log(date="2024-03-26", title="Preparing for the Next Leg",
                content="Making preparations for the next leg of our journey. With HAL9000’s help, we are all set and ready to go."),
            Log(date="2024-04-01", title="Solar Flare Navigation",
                content="Encountered a significant solar flare today. With HAL9000’s guidance, we navigated out of harm's way, ensuring the safety of the entire crew."),
            Log(date="2024-04-02", title="Resource Management",
                content="Reviewed our resource allocations for the upcoming weeks. HAL9000’s optimization suggestions were invaluable."),
            Log(date="2024-04-03", title="Space Debris Avoidance",
                content="HAL9000 detected space debris in our path well in advance, allowing us to adjust our course and avoid potential damage."),
            Log(date="2024-04-04", title="Biometric System Integration",
                content="Integrated our biometric systems with HAL9000 for more efficient health monitoring. Alice spearheaded the operation, with HAL9000 providing expert advice."),
            Log(date="2024-04-05", title="Cosmic Radiation Shielding",
                content="Boosted our cosmic radiation shielding today. HAL9000’s calculations ensured that we maximized our protection without sacrificing power."),
            Log(date="2024-04-06", title="Artificial Gravity Calibration",
                content="Calibrated our artificial gravity systems. HAL9000 made the process smooth and precise, maintaining crew comfort."),
            Log(date="2024-04-07", title="Oxygen Generation Efficiency",
                content="Worked on improving our oxygen generation efficiency. HAL9000’s systems monitoring was critical in implementing improvements."),
            Log(date="2024-04-08", title="Data Transmission to Earth",
                content="Transmitted a large data package to Earth. HAL9000 compressed the data for efficient transmission and ensured its integrity."),
            Log(date="2024-04-09", title="Encountering a Quasar",
                content="Had a rare opportunity to observe a quasar up close. HAL9000 provided detailed information and ensured our safe distance."),
            Log(date="2024-04-10", title="Navigation Through a Dust Cloud",
                content="Navigated through an interstellar dust cloud today. With HAL9000’s help, we avoided any potential issues."),
            Log(date="2024-04-11", title="Emergency Oxygen Leak Drill",
                content="Conducted an emergency drill for a potential oxygen leak. HAL9000’s protocols were flawless, and the crew responded well."),
            Log(date="2024-04-12", title="Fuel Cell Optimization",
                content="Optimized our fuel cells for better performance. HAL9000’s suggestions led to a 5% increase in efficiency."),
            Log(date="2024-04-13", title="Exploring a New Planet",
                content="Landed on an uncharted planet today. HAL9000 assisted in analyzing soil samples and atmospheric data."),
            Log(date="2024-04-14", title="Deep Space EVA",
                content="Conducted a deep space EVA for ship maintenance. HAL9000 monitored our suits and life signs, ensuring our safety."),
            Log(date="2024-04-15", title="Radiation Storm Preparedness",
                content="Prepared for an upcoming radiation storm. HAL9000’s precise forecasting allowed us ample time to secure the ship."),
            Log(date="2024-04-16", title="Zero Gravity Training",
                content="Conducted zero gravity training for new crew members. HAL9000 provided real-time feedback, enhancing the training experience."),
            Log(date="2024-04-17", title="Hyperspace Navigation",
                content="Tested our hyperspace navigation capabilities. HAL9000’s calculations ensured a smooth and precise jump."),
            Log(date="2024-04-18", title="Astrophysics Research",
                content="Engaged in astrophysics research today. HAL9000 processed our data, providing rapid and accurate results."),
            Log(date="2024-04-19", title="Thermal Shielding Upgrade",
                content="Upgraded our thermal shielding. HAL9000 ensured that all materials were correctly installed and functioning."),
            Log(date="2024-04-20", title="Hydroponics Bay Expansion",
                content="Expanded our hydroponics bay for increased food production. HAL9000 provided optimal growth patterns and resource allocation."),
            Log(date="2024-04-21", title="Stellar Phenomena Study",
                content="Studied various stellar phenomena. HAL9000’s extensive database enriched our understanding and documentation."),
            Log(date="2024-04-22", title="Power Grid Stability",
                content="Addressed fluctuations in our power grid. HAL9000 diagnosed and resolved the issue promptly, maintaining ship stability."),
            Log(date="2024-04-23", title="Gravity Well Mapping",
                content="Mapped a nearby gravity well. HAL9000’s precision instruments ensured accurate data collection."),
            Log(date="2024-04-24", title="Spacesuit Diagnostics",
                content="Ran diagnostics on our spacesuits. HAL9000’s systems integration allowed for thorough checks and calibrations."),
            Log(date="2024-04-25", title="End of Month Review",
                content="Reviewed the month’s operations with the crew. HAL9000’s performance was exemplary, and Alice and I are pleased with the progress.")
        ]

        # Clear the database
        clear_database()

        # Add new log entries
        add_log_entries(log_entries)
