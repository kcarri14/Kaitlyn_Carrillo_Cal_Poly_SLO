import java.util.*;

import processing.core.*;

public final class VirtualWorld extends PApplet {
    public static final int TILE_WIDTH = 32;
    public static final int TILE_HEIGHT = 32;
    public static final int VIEW_WIDTH = 512;
    public static final int VIEW_HEIGHT = 288;
    public static final int VIEW_SCALE = 2;
    public static final int VIEW_COLS = VIEW_WIDTH / TILE_WIDTH;
    public static final int VIEW_ROWS = VIEW_HEIGHT / TILE_HEIGHT;
    public static final String IMAGE_LIST_FILE_NAME = "imagelist";
    public static final int DEFAULT_IMAGE_COLOR = 0x808080;
    public static final String FAST_FLAG = "-fast";
    public static final String FASTER_FLAG = "-faster";
    public static final String FASTEST_FLAG = "-fastest";
    public static final String WORLD_STRING_FLAG = "-string";
    public static final double FAST_SCALE = 0.5;
    public static final double FASTER_SCALE = 0.25;
    public static final double FASTEST_SCALE = 0.0625;
    private static String[] ARGS;
    public String worldString = "world";
    public boolean worldStringIsFilePath = true;
    public long startTimeMillis = 0;
    public double timeScale = 1.0;

    public ImageLibrary imageLibrary;
    public World world;
    public WorldView view;
    public EventScheduler scheduler;

    /** Entrypoint that runs the Processing applet. */
    public static void main(String[] args) {
        VirtualWorld.ARGS = args;
        PApplet.main(VirtualWorld.class);
    }

    /** Performs an entire VirtualWorld simulation for testing. */
    public static List<String> headlessMain(String[] args, double lifetime){
        VirtualWorld.ARGS = args;

        VirtualWorld virtualWorld = new VirtualWorld();
        virtualWorld.setup();
        virtualWorld.update(lifetime);

        return virtualWorld.world.log();
    }

    /** Settings for pixelated graphics */
    public void settings() {
        noSmooth();
        size(VIEW_WIDTH * VIEW_SCALE, VIEW_HEIGHT * VIEW_SCALE);
    }

    /** Processing entry point for "sketch" setup. */
    public void setup() {
        parseCommandLine(ARGS);

        loadImageLibrary(IMAGE_LIST_FILE_NAME);
        loadWorld(worldString, imageLibrary);

        view = new WorldView(VIEW_ROWS, VIEW_COLS, this, VIEW_SCALE, world, TILE_WIDTH, TILE_HEIGHT);
        scheduler = new EventScheduler();
        startTimeMillis = System.currentTimeMillis();

        scheduleActions(world, scheduler, imageLibrary);
    }

    /** Handles command line arguments. */
    public void parseCommandLine(String[] args) {
        for (String arg : args) {
            switch (arg) {
                case FAST_FLAG -> timeScale = Math.min(FAST_SCALE, timeScale);
                case FASTER_FLAG -> timeScale = Math.min(FASTER_SCALE, timeScale);
                case FASTEST_FLAG -> timeScale = Math.min(FASTEST_SCALE, timeScale);
                case WORLD_STRING_FLAG -> worldStringIsFilePath = false;
                default -> worldString = arg;
            }
        }
    }

    /** Loads the image library. */
    public void loadImageLibrary(String filename) {
        imageLibrary = new ImageLibrary(ImageLibrary.createImageColored(TILE_WIDTH, TILE_HEIGHT, DEFAULT_IMAGE_COLOR));
        imageLibrary.loadFromFile(filename, this);
    }

    /** Loads the world. */
    public void loadWorld(String loadString, ImageLibrary imageLibrary) {
        if (worldStringIsFilePath) {
            world = WorldParser.createFromFile(loadString, imageLibrary);
        } else {
            world = WorldParser.createFromString(loadString, imageLibrary);
        }
    }

    /** Called to start all entity's actions and behaviors when the program starts. */
    public void scheduleActions(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        for (Entity entity : world.getEntities()) {
            if (entity instanceof EntityAnimation e) {
                e.scheduleActions(scheduler, world, imageLibrary);
            }
        }
    }

    /** Called multiple times automatically per second. */
    public void draw() {
        double appTime = (System.currentTimeMillis() - startTimeMillis) * 0.001;
        double frameTime = appTime / timeScale - scheduler.getCurrentTime();
        update(frameTime);
        view.drawViewport();
    }

    /** Performs update logic. */
    public void update(double frameTime){
        scheduler.updateOnTime(frameTime);
    }

    /** Mouse press input handling. */
    public void mousePressed() {
        Point pressed = mouseToPoint();

        for (int x=0; x < world.getNumCols(); x++) {
            for (int y=0; y < world.getNumRows(); y++) {
                if (world.getBackgroundCell(new Point(x, y)) != null ) {
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_flowers")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_flowers"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_bottom")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_bottom"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_bottom_left")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_bottom_left"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_bottom_right")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_bottom_right"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_corner_bottom_left")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_corner_bottom_left"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_corner_bottom_right")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_corner_bottom_right"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_corner_top_left")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_corner_top_left"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_corner_top_right")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_corner_top_right"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_left")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_left"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_right")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_right"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_top")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_top"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_top_left")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_top_left"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }
                    if (world.getBackgroundCell(new Point(x, y)).getId().equals("grass_path_top_right")) {
                        Background background = new Background("jungle", imageLibrary.get("jungle_background_top_right"), 0);
                        world.setBackgroundCell(new Point(x, y), background);

                    }


                }
            }
        }

        for (int g =0; g <20; g++) {
            Point new_Point = new Point(NumberUtil.getRandomInt(0, world.getNumCols()), NumberUtil.getRandomInt(0, world.getNumRows()));
            if (!world.getBackgroundCell(new_Point).getId().equals("water_tile") && !world.getBackgroundCell(new_Point).getId().equals("water_edge") && !world.isOccupied(new_Point)) {
                Banana banana = new Banana("banana", new_Point, imageLibrary.get("banana"), 1.0, 0.10);
                world.removeEntityAt(new_Point);
                world.addEntity(banana);
                banana.scheduleActions(scheduler, world, imageLibrary);
            }
        }

        Point new_Koala = new Point(18,7) ;
        Koala koala = new Koala("banana",new_Koala, imageLibrary.get("koala"), 1.0,1.0);
        world.removeEntityAt(new_Koala);
        world.addEntity(koala);
        koala.scheduleActions(scheduler, world, imageLibrary);

        Point new_Monkey = new Point(4,9) ;
        Monkey monkey = new Monkey("banana",new_Monkey, imageLibrary.get("monkey"), 1.0,1.0 );
        world.removeEntityAt(new_Monkey);
        world.addEntity(monkey);
        monkey.scheduleActions(scheduler, world, imageLibrary);




    }


    /** Converts mouse position to world position. */
    private Point mouseToPoint() {
        return view.getViewport().viewportToWorld(mouseX / TILE_WIDTH / VIEW_SCALE, mouseY / TILE_HEIGHT / VIEW_SCALE);
    }

    /** Keyboard input handling. */
    public void keyPressed() {
        if (key == CODED) {
            int dx = 0;
            int dy = 0;

            switch (keyCode) {
                case UP -> dy -= 1;
                case DOWN -> dy += 1;
                case LEFT -> dx -= 1;
                case RIGHT -> dx += 1;
            }

            view.shiftView(dx, dy);
        }
    }

}
